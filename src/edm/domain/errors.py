import typing

from edm.domain import value_objects
from edm.domain.entities import base as base_entities


class DomainError(Exception):
    pass


class InvalidTransition(DomainError):
    def __init__(
        self,
        from_status: value_objects.PackageStatus,
        to_status: value_objects.PackageStatus,
        valid_new_statuses: typing.Set[value_objects.PackageStatus],
        *args: object,
        reason: typing.Text | None = None,
        is_recover: bool = False,
    ) -> None:
        transition_type = "Transition" if not is_recover else "Recover transition"
        message = f"{transition_type} from `{from_status}` to `{to_status}` is not allowed. Allowed transitions: `{valid_new_statuses}`"
        if reason:
            message += f". Reason: {reason}"

        super().__init__(message, *args)


class UnrecoverableAggregateState(DomainError):
    def __init__(self, aggregate: base_entities.Aggregate, *args: object) -> None:
        message = f"Aggregate is in unrecoverable state. Aggregate: `{aggregate.model_dump_json()}`"
        super().__init__(message, *args)


class AggregateExpired(DomainError):
    def __init__(self, aggregate: base_entities.Aggregate, *args: object) -> None:
        message = f"Aggregate has expired. Aggregate: `{aggregate.model_dump_json()}`"
        super().__init__(message, *args)


class InvalidEntityId(DomainError):
    def __init__(
        self,
        entity_name: typing.Text,
        requested_id: typing.Text,
        possible_ids: typing.Sequence[typing.Text],
        *args: object,
    ) -> None:
        message = f"Invalid `{entity_name}` entity id provided : `{requested_id}`. Possible ids: `{possible_ids}`"
        super().__init__(message, *args)
