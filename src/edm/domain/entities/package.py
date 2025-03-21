import datetime
import functools
import typing
import uuid

import pydantic
from loguru import logger

from edm.domain import errors, events, value_objects
from edm.domain.entities import base as base_entities
from edm.domain.entities import document as document_entities
from edm.domain.entities import file as file_entities

_T = typing.TypeVar("_T")
_P = typing.ParamSpec("_P")


class Package(base_entities.Aggregate):
    counterparty: value_objects.Counterparty = pydantic.Field(frozen=True)
    for_sign: pydantic.StrictBool
    documents: typing.Mapping[uuid.UUID, document_entities.Document]

    status: value_objects.PackageStatus = pydantic.Field(default=value_objects.PackageStatus.DRAFT)
    failure_status: value_objects.FailureStatus = pydantic.Field(default=value_objects.FailureStatus.NoFailure)
    failure_reason: pydantic.StrictStr = pydantic.Field(default="")

    expiration_date: datetime.datetime = pydantic.Field(
        default_factory=lambda: datetime.datetime.now() + datetime.timedelta(days=365),
        frozen=True,
    )

    _valid_status_transitions: typing.Dict[value_objects.PackageStatus, typing.Set[value_objects.PackageStatus]] = (
        pydantic.PrivateAttr(
            default={
                value_objects.PackageStatus.DRAFT: {value_objects.PackageStatus.CREATED},
                value_objects.PackageStatus.CREATED: {value_objects.PackageStatus.QUEUED},
                value_objects.PackageStatus.QUEUED: {value_objects.PackageStatus.SENT},
                value_objects.PackageStatus.SENT: {value_objects.PackageStatus.SIGNED},
                value_objects.PackageStatus.SIGNED: {value_objects.PackageStatus.SIGNED_DOWNLOADED},
            },
        )
    )

    _valid_status_recover_transitions: typing.Dict[
        value_objects.PackageStatus,
        typing.Set[value_objects.PackageStatus],
    ] = pydantic.PrivateAttr(
        default={
            value_objects.PackageStatus.QUEUED: {value_objects.PackageStatus.QUEUED},
            value_objects.PackageStatus.SIGNED: {value_objects.PackageStatus.SIGNED},
        },
    )

    @pydantic.computed_field(return_type=bool)  # type: ignore[misc]
    @property
    def processed(self) -> bool:
        if self.failure_status in (value_objects.FailureStatus.CriticalFailure, value_objects.FailureStatus.Expired):
            return True

        match self.status:
            case value_objects.PackageStatus.DRAFT:
                return False
            case value_objects.PackageStatus.CREATED:
                return False
            case value_objects.PackageStatus.QUEUED:
                return False
            case value_objects.PackageStatus.SENT:
                return not self.for_sign
            case value_objects.PackageStatus.SIGNED:
                return False
            case value_objects.PackageStatus.SIGNED_DOWNLOADED:
                return True
            case _:
                raise ValueError(f"Unhandled package status during `processed` evaluation: {self.status}")

    @staticmethod
    def _transition_to_status(
        new_status: value_objects.PackageStatus,
    ) -> typing.Callable[
        [typing.Callable[typing.Concatenate["Package", _P], _T]],
        typing.Callable[typing.Concatenate["Package", _P], _T],
    ]:
        """
        Проверяет возможен ли переход из текущего статуса пакета в новый.
        После вызова декорируемой функции, если та не вызовет исключение, переводит пакет в новый статус.
        """

        def decorator(
            method: typing.Callable[typing.Concatenate["Package", _P], _T],
        ) -> typing.Callable[typing.Concatenate["Package", _P], _T]:
            @functools.wraps(method)
            def wrapper(self: "Package", *args: _P.args, **kwargs: _P.kwargs) -> _T:
                if self.failure_status is not value_objects.FailureStatus.NoFailure:
                    raise errors.InvalidTransition(
                        from_status=self.status,
                        to_status=new_status,
                        valid_new_statuses=set(),
                        reason="Package recovery required",
                    )

                valid_new_statuses = self._valid_status_transitions.get(self.status, set())
                if new_status not in valid_new_statuses:
                    raise errors.InvalidTransition(
                        from_status=self.status,
                        to_status=new_status,
                        valid_new_statuses=valid_new_statuses,
                    )

                old_status = self.status
                res = method(self, *args, **kwargs)
                self.status = new_status
                logger.info(f"Package `{self.guid}` has transitioned from `{old_status}` to `{new_status}`")
                return res

            return wrapper

        return decorator

    @staticmethod
    def _recover_to_status(
        new_status: value_objects.PackageStatus,
    ) -> typing.Callable[
        [typing.Callable[typing.Concatenate["Package", _P], _T]],
        typing.Callable[typing.Concatenate["Package", _P], _T],
    ]:
        """
        Проверяет возможен ли откат из текущего статуса пакета в новый.
        После вызова декорируемой функции, если та не вызовет исключение, переводит пакет в новый статус.
        """

        def decorator(
            method: typing.Callable[typing.Concatenate["Package", _P], _T],
        ) -> typing.Callable[typing.Concatenate["Package", _P], _T]:
            @functools.wraps(method)
            def wrapper(self: "Package", *args: _P.args, **kwargs: _P.kwargs) -> _T:
                if self.failure_status is value_objects.FailureStatus.NoFailure:
                    raise errors.InvalidTransition(
                        from_status=self.status,
                        to_status=new_status,
                        valid_new_statuses=set(),
                        reason="Package does not require recovery",
                        is_recover=True,
                    )

                valid_new_statuses = self._valid_status_recover_transitions.get(self.status, set())
                if new_status not in valid_new_statuses:
                    raise errors.InvalidTransition(
                        from_status=self.status,
                        to_status=new_status,
                        valid_new_statuses=valid_new_statuses,
                        is_recover=True,
                    )

                old_status = self.status
                res = method(self, *args, **kwargs)
                self.status = new_status
                logger.info(f"Package `{self.guid}` has recovered from `{old_status}` to `{new_status}`")
                return res

            return wrapper

        return decorator

    @staticmethod
    def _check_expiry(
        method: typing.Callable[typing.Concatenate["Package", _P], _T],
    ) -> typing.Callable[typing.Concatenate["Package", _P], _T]:
        """Проверяет релевантность пакета."""

        @functools.wraps(method)
        def wrapper(self: "Package", *args: _P.args, **kwargs: _P.kwargs) -> _T:
            expired = self.expiration_date < datetime.datetime.now()
            if expired:
                self.failure_status = value_objects.FailureStatus.Expired
                self.failure_reason = "Expired"
                raise errors.AggregateExpired(self)

            return method(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def _clear_failure_info_on_recover(
        method: typing.Callable[typing.Concatenate["Package", _P], _T],
    ) -> typing.Callable[typing.Concatenate["Package", _P], _T]:
        """Сбрасывает ошибки при успешном восстановлении пакета."""

        @functools.wraps(method)
        def wrapper(self: "Package", *args: _P.args, **kwargs: _P.kwargs) -> _T:
            res = method(self, *args, **kwargs)

            self.failure_reason = ""
            self.failure_status = value_objects.FailureStatus.NoFailure

            return res

        return wrapper

    @_transition_to_status(value_objects.PackageStatus.CREATED)
    def mark_as_created(self) -> None:
        self._register_event(events.PackageCreated(package_id=self.guid))

    @_transition_to_status(value_objects.PackageStatus.QUEUED)
    def mark_as_queued(self) -> None:
        self._register_event(events.PackageQueued(package_id=self.guid))

    @_clear_failure_info_on_recover
    @_check_expiry
    @_recover_to_status(value_objects.PackageStatus.QUEUED)
    def recover_to_queued(self) -> None:
        self._register_event(events.PackageQueued(package_id=self.guid))

    @_transition_to_status(value_objects.PackageStatus.SENT)
    def mark_as_sent(self) -> None:
        pass

    @_transition_to_status(value_objects.PackageStatus.SIGNED)
    def mark_as_signed(self) -> None:
        if not self.for_sign:
            raise errors.InvalidTransition(
                from_status=self.status,
                to_status=value_objects.PackageStatus.SIGNED,
                valid_new_statuses=set(),
                reason="Package is not for sign",
            )

        self._register_event(events.PackageSigned(package_id=self.guid))

    @_clear_failure_info_on_recover
    @_check_expiry
    @_recover_to_status(value_objects.PackageStatus.SIGNED)
    def recover_to_signed(self) -> None:
        self._register_event(events.PackageSigned(package_id=self.guid))

    @_transition_to_status(value_objects.PackageStatus.SIGNED_DOWNLOADED)
    def mark_as_signed_downloaded(self) -> None:
        self._register_event(events.PackageSignedDownloaded(package_id=self.guid))

    def mark_as_failed(self, reason: typing.Text, should_try_again: bool) -> None:
        self.failure_reason = reason

        if not should_try_again:
            self.failure_status = value_objects.FailureStatus.CriticalFailure
        else:
            self.failure_status = value_objects.FailureStatus.Failure
            self._register_event(event=events.PackageProcessingFailed(package_id=self.guid))

        logger.info(f"Packge `{self.guid}` marked as failed. Reason: {reason}")

    def set_external_file_id_for_document(self, document_id: uuid.UUID, external_file_id: typing.Text) -> None:
        try:
            self.documents[document_id].set_external_file_id(external_file_id)
        except KeyError:
            raise errors.InvalidEntityId(
                document_entities.Document.__name__,
                str(document_id),
                possible_ids=list(map(lambda x: str(x), self.documents.keys())),
            )

    def set_signed_file_for_document(self, document_id: uuid.UUID, signed_file: file_entities.File) -> None:
        try:
            self.documents[document_id].set_file_signed(signed_file)
        except KeyError:
            raise errors.InvalidEntityId(
                document_entities.Document.__name__,
                str(document_id),
                possible_ids=list(map(lambda x: str(x), self.documents.keys())),
            )
