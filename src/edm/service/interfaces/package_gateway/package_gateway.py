import abc
import typing
import uuid

import pydantic

from edm.domain.entities import document as document_entities
from edm.domain.entities import package as package_entities
from edm.service.models import read as read_models

DocumentId: typing.TypeAlias = uuid.UUID
ExternalFileId: typing.TypeAlias = pydantic.StrictStr | None
SendResult: typing.TypeAlias = typing.Mapping[DocumentId, ExternalFileId]


class PackageGatewayRead(abc.ABC):
    """Шлюз для взаимодействия с пакетами (только чтение)."""

    @abc.abstractmethod
    async def is_package_signed(self, package: package_entities.Package) -> bool:
        pass

    @abc.abstractmethod
    async def download_signed_file(self, document: document_entities.Document) -> read_models.FileHydrated:
        pass


class PackageGateway(PackageGatewayRead):
    """
    Шлюз для взаимодействия с пакетами.

    Обеспечивает функциональность передачи/получения файлов внешней СДО.
    """

    @abc.abstractmethod
    async def send(self, package: read_models.PackageHydrated) -> SendResult:
        pass
