import contextlib
import typing

from edm.service.interfaces import uow as interface


class InMemoryOutboxedPackageUow(interface.OutboxedPackageUow):
    @contextlib.asynccontextmanager
    async def _transaction(
        self,
    ) -> typing.AsyncIterator[tuple[typing.Self, interface.OutboxedPackageUowRepositroies]]:
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
