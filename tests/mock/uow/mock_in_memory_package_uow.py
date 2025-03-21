import asyncio
import contextlib
import typing

from edm.service.interfaces import repositories as repository_interfaces
from edm.service.interfaces import uow as interface


class MockInMemoryPackageUow(interface.PackageUow):
    # Глобальный лок, чтобы обеспечить транзакционность чтения глобальной переменной репозитория _packages
    # Это своего рода единственная альтернатива сессий для in-memory реализации
    _global_lock = asyncio.Lock()

    def __init__(self, package_repository: repository_interfaces.PackageRepository) -> None:
        super().__init__(package_repository)

    @contextlib.asynccontextmanager
    async def transaction(self) -> typing.AsyncIterator[tuple[typing.Self, repository_interfaces.PackageRepository]]:
        async with self._global_lock:
            try:
                yield self, self._package_repository
            finally:
                await self._rollback()

    async def _commit(self) -> None:
        await self._package_repository.commit()

    async def _rollback(self) -> None:
        await self._package_repository.rollback()
