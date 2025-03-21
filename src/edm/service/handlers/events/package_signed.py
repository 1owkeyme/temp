import cqrs

from edm.domain import errors as domain_errors
from edm.domain import events
from edm.service import errors
from edm.service.interfaces import file_storage as file_storage_interfaces
from edm.service.interfaces import package_gateway as package_gateway_interfaces
from edm.service.interfaces import uow as uow_interfaces


class PackageSignedHandler(cqrs.EventHandler[cqrs.NotificationEvent[events.PackageSigned]]):
    """
    Обработчик доменного события PackageSigned.

    Когда пакет становится подписанным, он скачивается.
    """

    def __init__(
        self,
        outboxed_package_uow: uow_interfaces.OutboxedPackageUow,
        file_storage: file_storage_interfaces.FileStorage,
        package_gateway: package_gateway_interfaces.PackageGateway,
    ) -> None:
        self._outboxed_package_uow = outboxed_package_uow
        self._file_storage = file_storage
        self._package_gateway = package_gateway

    async def handle(self, event: cqrs.NotificationEvent[events.PackageSigned]) -> None:
        async with self._outboxed_package_uow.transaction() as (outboxed_package_uow, repositories):
            package = await repositories.package_repository.get_by_id(event.payload.package_id)

            if package is None:
                raise errors.PackageNotFound(package_id=str(event.payload.package_id))

            for document_id, document in package.documents.items():
                try:
                    signed_file_hydrated = await self._package_gateway.download_signed_file(document)
                except package_gateway_interfaces.errors.PackageDownloadFailed as exc:
                    package.mark_as_failed(reason=str(exc), should_try_again=exc.should_try_again)
                    break

                else:
                    signed_file = signed_file_hydrated.to_entity()
                    download_url = await self._file_storage.upload_downloadable(signed_file_hydrated)
                    signed_file.set_download_url(download_url)
                    package.set_signed_file_for_document(document_id, signed_file)

            else:
                try:
                    package.mark_as_signed_downloaded()
                except domain_errors.InvalidTransition as exc:
                    package.mark_as_failed(reason=str(exc), should_try_again=False)

            await repositories.package_repository.save(package)
            await outboxed_package_uow.commit()
