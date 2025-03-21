import uuid

from edm.domain.entities import document as document_entities
from edm.domain.entities import package as package_entities
from edm.service.interfaces import package_gateway as interfaces
from edm.service.models import read as read_models


class InMemoryPackageGateway(interfaces.PackageGateway):
    def __init__(self):
        self._packages: dict[uuid.UUID, read_models.PackageHydrated] = {}
        self._signed_files: dict[uuid.UUID, read_models.FileHydrated] = {}

    async def is_package_signed(self, package: package_entities.Package) -> bool:
        stored_package = self._packages.get(package.guid)

        if not stored_package:
            return False

        return all(doc.file_signed is not None for doc in stored_package.documents)

    async def download_signed_file(self, document: document_entities.Document) -> read_models.FileHydrated:
        if document.guid in self._signed_files:
            return self._signed_files[document.guid]

        raise FileNotFoundError(f"Signed file for document {document.guid} not found")

    async def send(self, package: read_models.PackageHydrated) -> interfaces.package_gateway.SendResult:
        self._packages[package.guid] = package

        result = {doc.guid: f"external-file-id-{doc.guid}" for doc in package.documents}
        return result
