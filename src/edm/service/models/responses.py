import typing
import uuid

import pydantic
from cqrs import response

from edm.domain import value_objects
from edm.domain.entities import document as document_entities
from edm.domain.entities import file as file_entities
from edm.domain.entities import package as package_entities


class Guid(pydantic.BaseModel):
    guid: uuid.UUID = pydantic.Field(description="UUID идентификатор")


class File(Guid):
    name: pydantic.StrictStr = pydantic.Field(description="Имя файла", examples=["important.pdf"])
    download_url: pydantic.AnyUrl | None = pydantic.Field(description="Ссылка на скачивание файла")

    @classmethod
    def from_entity(cls, entity: file_entities.File) -> typing.Self:
        return cls(guid=entity.guid, name=entity.name, download_url=entity.download_url)


class Files(response.Response):
    sent_file: File = pydantic.Field(description="Высланный файл документа")
    signed_file: File | None = pydantic.Field(None, description="Подписанный файл документа")

    @classmethod
    def from_document(cls, document: document_entities.Document) -> typing.Self:
        sent_file = File.from_entity(document.file)
        signed_file = File.from_entity(document.file_signed) if document.file_signed else None
        return cls(sent_file=sent_file, signed_file=signed_file)


class Document(Guid):
    status: value_objects.PackageStatus = pydantic.Field(description="Статус документа")
    files: Files

    @classmethod
    def from_entity(
        cls,
        document: document_entities.Document,
        package_status: value_objects.PackageStatus,
    ) -> typing.Self:
        return cls(guid=document.guid, status=package_status, files=Files.from_document(document))


class PackageCreated(response.Response):
    package_guid: uuid.UUID = pydantic.Field(description="Уникальный идентификатор пакета документов в системе EDM")


class ProcessFailedPackages(response.Response):
    pass


class ProcessPackages(response.Response):
    pass


class GetDocuments(response.Response):
    documents: typing.Sequence[Document] = pydantic.Field(description="Документы")

    @classmethod
    def from_packages(cls, packages: typing.Sequence[package_entities.Package]) -> typing.Self:
        documents: typing.List[Document] = []
        for package in packages:
            for document in package.documents.values():
                documents.append(Document.from_entity(document, package_status=package.status))
        return cls(documents=documents)


class GetDocumentById(response.Response):
    document: Document | None = pydantic.Field(description="Документ или null")


class ResendDocument(response.Response):
    pass
