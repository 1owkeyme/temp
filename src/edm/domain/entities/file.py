import pydantic

from edm.domain.entities import base as base_entities

MIN_FILE_NAME_LENGTH = 1
MAX_FILE_NAME_LENGTH = 2**8
FILE_NAME_REGEX = r"^[\S]+$"


class File(base_entities.Entity):
    name: pydantic.StrictStr = pydantic.Field(
        min_length=MIN_FILE_NAME_LENGTH,
        max_length=MAX_FILE_NAME_LENGTH,
        pattern=FILE_NAME_REGEX,
        frozen=True,
    )
    download_url: pydantic.AnyUrl | None

    def set_download_url(self, download_url: pydantic.AnyUrl) -> None:
        self.download_url = download_url
