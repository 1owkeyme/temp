import pydantic

from edm.domain.entities import base as base_entities
from edm.domain.entities import file as file_entities


class Document(base_entities.Entity):
    external_file_id: pydantic.StrictStr | None

    file: file_entities.File
    file_signed: file_entities.File | None

    def set_file_signed(self, file_signed: file_entities.File) -> None:
        self.file_signed = file_signed

    def set_external_file_id(self, external_file_id: pydantic.StrictStr) -> None:
        self.external_file_id = external_file_id
