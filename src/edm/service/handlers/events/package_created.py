import cqrs

from edm.domain import errors as domain_errors
from edm.domain import events
from edm.service import errors
from edm.service.interfaces import uow as uow_interfaces


class PackageCreatedHandler(cqrs.EventHandler[cqrs.NotificationEvent[events.PackageCreated]]):
    """
    Обработчик доменного события PackageCreated.

    Когда пакет создан, он ставится в очередь на отправку.

    Этот обработчик промежуточный. Существует для того, чтобы в будущем было легко добавлять реальный юзкейс.
    """

    def __init__(self, outboxed_package_uow: uow_interfaces.OutboxedPackageUow) -> None:
        self._outboxed_package_uow = outboxed_package_uow

    async def handle(self, event: cqrs.NotificationEvent[events.PackageCreated]) -> None:
        async with self._outboxed_package_uow.transaction() as (outboxed_package_uow, repositories):
            package = await repositories.package_repository.get_by_id(event.payload.package_id)

            if package is None:
                raise errors.PackageNotFound(package_id=str(event.payload.package_id))

            try:
                package.mark_as_queued()
            except domain_errors.InvalidTransition as exc:
                package.mark_as_failed(reason=str(exc), should_try_again=False)

            await repositories.package_repository.save(package)
            await outboxed_package_uow.commit()
