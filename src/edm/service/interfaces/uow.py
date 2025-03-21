import abc
import contextlib
import typing

import cqrs

from edm.domain.entities import base as base_entities
from edm.service import events
from edm.service.interfaces import repositories as repository_interfaces


class Uow(abc.ABC):
    async def commit(self) -> None:
        await self._commit()

    @abc.abstractmethod
    async def _commit(self) -> None:
        pass

    @abc.abstractmethod
    async def _rollback(self) -> None:
        pass


class PackageUow(Uow):
    def __init__(self, package_repository: repository_interfaces.PackageRepository) -> None:
        self._package_repository = package_repository

    @abc.abstractmethod
    @contextlib.asynccontextmanager
    def transaction(self) -> typing.AsyncIterator[tuple[typing.Self, repository_interfaces.PackageRepository]]:
        pass


class OutboxedUowRepositroies(abc.ABC):
    def __init__(self, outboxed_event_repository: cqrs.OutboxedEventRepository) -> None:
        self._outboxed_event_repository = outboxed_event_repository

    @property
    def outboxed_event_repository(self) -> cqrs.OutboxedEventRepository:
        return self._outboxed_event_repository

    @abc.abstractmethod
    def get_seen_aggregates(self) -> typing.Sequence[base_entities.Aggregate]:
        pass


_TRepositories = typing.TypeVar("_TRepositories", bound=OutboxedUowRepositroies)


# _Ts = typing.TypeVarTuple("_Ts")

# # Это необходимый type-guard, т.к. на данный момент в PEP-646 решили не делать поддержку bound для TypeVarTuple:
# # https://peps.python.org/pep-0646/#variance-type-constraints-and-type-bounds-not-yet-supported
# if not isinstance(repository, interfaces.repositories.base.RepositoryBase):
#     raise TypeError
# class OutboxedUow(typing.Generic[*_Ts], Uow):
# (_,*repositories,outbox_repository) = transaction


class OutboxedUow(typing.Generic[_TRepositories], Uow):
    def __init__(self, repositories: _TRepositories) -> None:
        super().__init__()
        self._repositories = repositories

    @contextlib.asynccontextmanager
    async def transaction(self) -> typing.AsyncIterator[tuple[typing.Self, _TRepositories]]:
        async with self._transaction() as transaction:
            yield transaction
            (_, repositories) = transaction

            for aggregate in repositories.get_seen_aggregates():
                for event in aggregate.events:
                    domain_event_type = event.__class__

                    repositories.outboxed_event_repository.add(
                        cqrs.NotificationEvent[domain_event_type](
                            event_name=events.get_service_event_name(domain_event_type),
                            payload=event,
                        ),
                    )

        await self._rollback()

    @abc.abstractmethod
    @contextlib.asynccontextmanager
    def _transaction(self) -> typing.AsyncIterator[tuple[typing.Self, _TRepositories]]:
        pass


class OutboxedPackageUowRepositroies(OutboxedUowRepositroies):
    def __init__(
        self,
        outboxed_event_repository: cqrs.OutboxedEventRepository,
        package_repository: repository_interfaces.PackageRepository,
    ) -> None:
        super().__init__(outboxed_event_repository)
        self._package_repository = package_repository

    def get_seen_aggregates(self) -> typing.Sequence[base_entities.Aggregate]:
        return [*self._package_repository.seen_aggregates]

    @property
    def package_repository(self) -> repository_interfaces.PackageRepository:
        return self._package_repository


class OutboxedPackageUow(OutboxedUow[OutboxedPackageUowRepositroies]):
    pass
