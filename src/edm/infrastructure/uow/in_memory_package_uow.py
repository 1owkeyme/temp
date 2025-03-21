import contextlib
import typing

from edm.service.interfaces import repositories as repository_interfaces
from edm.service.interfaces import uow as interface


class InMemoryPackageUow(interface.PackageUow):
    @contextlib.asynccontextmanager
    async def transaction(self) -> typing.AsyncIterator[tuple[typing.Self, repository_interfaces.PackageRepository]]:
        try:
            yield self, self._package_repository
        finally:
            await self._rollback()

    async def _commit(self) -> None:
        await self._package_repository.commit()

    async def _rollback(self) -> None:
        await self._package_repository.rollback()
