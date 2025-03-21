import typing
import uuid

import cqrs

from edm.domain import errors as domain_errors
from edm.domain.entities import document as document_entities
from edm.domain.entities import file as file_entities
from edm.domain.entities import package as package_entities
from edm.service.interfaces import factories as factory_interfaces
from edm.service.models import commands, responses
from edm.service.models import read as read_models


class CreatePackageHandler(cqrs.RequestHandler[commands.CreatePackage, responses.PackageCreated]):
    """
    Обработчик команды CreatePackage.


    Создает аггрегат пакета документа, тем самым запуская его обработку.
    """

    def __init__(
        self,
        file_storage_factory: factory_interfaces.FileStorageFactory,  # TODO: возможно тут не нужна фактори
        outboxed_package_uow_factory: factory_interfaces.OutboxedPackageUowFactory,
    ) -> None:
        self._file_storage = file_storage_factory()
        self._outboxed_package_uow = outboxed_package_uow_factory()

    @property
    def events(self) -> typing.List[cqrs.Event]:
        return []

    async def handle(self, request: commands.CreatePackage) -> responses.PackageCreated:
        # Намеренно проводим операции со storage вне транзакции, т.к.
        # файловое хранилище обычно не предоставляет протокола транзакций.
        documents: typing.Dict[uuid.UUID, document_entities.Document] = {}
        for file_name, content in request.file_names_to_contents.items():
            file = file_entities.File(name=file_name, download_url=None)
            file_hydrated = read_models.FileHydrated.from_entity(file, content=content)
            download_url = await self._file_storage.upload_downloadable(file_hydrated)
            file.set_download_url(download_url)
            document = document_entities.Document(
                file=file,
                file_signed=None,
                external_file_id=None,
            )
            documents[document.guid] = document

        async with self._outboxed_package_uow.transaction() as (outboxed_package_uow, repositroies):
            package = package_entities.Package(
                documents=documents,
                counterparty=request.counterparty,
                for_sign=request.for_sign,
            )

            try:
                package.mark_as_created()
            except domain_errors.InvalidTransition as exc:
                package.mark_as_failed(reason=str(exc), should_try_again=False)

            await repositroies.package_repository.save(package)
            await outboxed_package_uow.commit()

        return responses.PackageCreated.model_construct(package_guid=package.guid)
