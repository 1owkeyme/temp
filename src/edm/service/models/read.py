import typing
import uuid

import pydantic

from edm.domain import value_objects
from edm.domain.entities import file as file_entities


class ReadModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(frozen=True)


class Guid(pydantic.BaseModel):
    guid: uuid.UUID


class FileHydrated(Guid):
    name: pydantic.StrictStr
    content: bytes

    def to_entity(self) -> file_entities.File:
        return file_entities.File(guid=self.guid, name=self.name, download_url=None)

    @classmethod
    def from_entity(cls, entity: file_entities.File, content: bytes) -> typing.Self:
        return cls(guid=entity.guid, name=entity.name, content=content)


class DocumentHydrated(Guid):
    external_file_id: pydantic.StrictStr | None

    file: FileHydrated
    file_signed: FileHydrated | None


class PackageHydrated(Guid):
    counterparty: value_objects.Counterparty
    status: value_objects.PackageStatus
    for_sign: pydantic.StrictBool
    documents: typing.List[DocumentHydrated]
