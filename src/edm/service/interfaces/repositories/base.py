import abc
import typing

from edm.domain.entities import base as base_entities

_T = typing.TypeVar("_T", bound=base_entities.Aggregate)


class Repostiory(abc.ABC, typing.Generic[_T]):
    def __init__(self) -> None:
        self._seen_aggregates: typing.List[_T] = []
        super().__init__()

    async def save(self, package: _T) -> None:
        self._seen_aggregates.append(package)
        await self._save(package)

    @property
    def seen_aggregates(self) -> typing.List[_T]:
        return self._seen_aggregates

    @abc.abstractmethod
    async def commit(self) -> None:
        pass

    @abc.abstractmethod
    async def rollback(self) -> None:
        pass

    @abc.abstractmethod
    async def _save(self, package: _T) -> None:
        pass
