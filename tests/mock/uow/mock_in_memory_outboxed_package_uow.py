import asyncio
import contextlib
import typing

from edm.service.interfaces import uow as interface


class MockInMemoryOutboxedPackageUow(interface.OutboxedPackageUow):
    # Глобальный лок, чтобы обеспечить транзакционность чтения глобальной переменной репозитория _packages
    # Это своего рода единственная альтернатива сессий для in-memory реализации
    _global_lock = asyncio.Lock()

    @contextlib.asynccontextmanager
    async def _transaction(
        self,
    ) -> typing.AsyncIterator[tuple[typing.Self, interface.OutboxedPackageUowRepositroies]]:
        async with self._global_lock:
            try:
                yield self, self._repositories
                await self._repositories.outboxed_event_repository.commit()
                await self._repositories.package_repository.commit()
            except Exception:
                await self._rollback()
                raise

    async def _commit(self) -> None:
        await self._repositories.outboxed_event_repository.commit()
        await self._repositories.package_repository.commit()

    async def _rollback(self) -> None:
        await self._repositories.outboxed_event_repository.rollback()
        await self._repositories.package_repository.rollback()
