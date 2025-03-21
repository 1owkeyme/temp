import cqrs

from edm.domain import errors as domain_errors
from edm.domain import events
from edm.service import errors
from edm.service.interfaces import file_storage as file_storage_interfaces
from edm.service.interfaces import package_gateway as package_gateway_interfaces
from edm.service.interfaces import uow as uow_interfaces
from edm.service.services import hydration


class PackageQueuedHandler(cqrs.EventHandler[cqrs.NotificationEvent[events.PackageQueued]]):
    """
    Обработчик доменного события PackageQueued.

    Когда пакет становится в очередь, он высылается контрагенту.
    """

    def __init__(
        self,
        outboxed_package_uow: uow_interfaces.OutboxedPackageUow,
        file_storage_read: file_storage_interfaces.FileStorageRead,
        package_gateway: package_gateway_interfaces.PackageGateway,
    ) -> None:
        self._outboxed_package_uow = outboxed_package_uow
        self._file_storage_read = file_storage_read
        self._package_gateway = package_gateway

    async def handle(self, event: cqrs.NotificationEvent[events.PackageQueued]) -> None:
        async with self._outboxed_package_uow.transaction() as (outboxed_package_uow, repositories):
            hydration_service = hydration.HydrationService(
                package_repository_read=repositories.package_repository,
                file_storage_read=self._file_storage_read,
            )
            package = await repositories.package_repository.get_by_id(event.payload.package_id)

            if package is None:
                raise errors.PackageNotFound(package_id=str(event.payload.package_id))

            package_hydrated = await hydration_service.hydrate_package(package)

            try:
                send_result = await self._package_gateway.send(package_hydrated)

                for document_id, document in package.documents.items():
                    try:
                        external_file_id = send_result[document.guid]
                    except KeyError:
                        msg_exc = f"External file ID has not been set for document `{document.guid}` of package `{package.guid}`"
                        raise errors.IncompletePackageSend(msg_exc)

                    if external_file_id is None:
                        continue

                    package.set_external_file_id_for_document(document_id, external_file_id)
            except package_gateway_interfaces.errors.PackageSendFailed as exc:
                package.mark_as_failed(reason=str(exc), should_try_again=exc.should_try_again)

            else:
                try:
                    package.mark_as_sent()
                except domain_errors.InvalidTransition as exc:
                    package.mark_as_failed(reason=str(exc), should_try_again=False)

            await repositories.package_repository.save(package)
            await outboxed_package_uow.commit()
