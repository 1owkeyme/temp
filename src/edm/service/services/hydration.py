from edm.domain.entities import document as document_entities
from edm.domain.entities import file as file_entities
from edm.domain.entities import package as package_entities
from edm.service import errors
from edm.service.interfaces import file_storage as file_storage_interfaces
from edm.service.interfaces import repositories as repository_interfaces
from edm.service.models import read as read_models


class HydrationService:
    """
    Сервис, который гидратирует сущности.

    Под процессом гидратации сущности понимается процесс, в ходе которого
    ссылки на другие сущности резолвятся и вставляются в место указателя
    (известные синонимы: unwind, expand, flatten).
    """

    def __init__(
        self,
        package_repository_read: repository_interfaces.PackageRepositoryRead,
        file_storage_read: file_storage_interfaces.FileStorageRead,
    ):
        self._package_repository_read = package_repository_read
        self._file_storage_read = file_storage_read

    async def hydrate_package(self, package: package_entities.Package) -> read_models.PackageHydrated:
        documents_hydrated = [await self.hydrate_document(document) for document in package.documents.values()]

        return read_models.PackageHydrated(
            guid=package.guid,
            counterparty=package.counterparty,
            status=package.status,
            for_sign=package.for_sign,
            documents=documents_hydrated,
        )

    async def hydrate_document(self, document: document_entities.Document) -> read_models.DocumentHydrated:
        return read_models.DocumentHydrated(
            guid=document.guid,
            file=await self.hydrate_file(document.file),
            file_signed=await self.hydrate_file(document.file_signed) if document.file_signed else None,
            external_file_id=document.external_file_id,
        )

    async def hydrate_file(self, file: file_entities.File) -> read_models.FileHydrated:
        hydrated_file = await self._file_storage_read.get_by_id(file.guid)

        if hydrated_file is None:
            raise errors.FileNotFound(file_id=str(file.guid))

        return hydrated_file
