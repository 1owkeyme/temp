import typing
import uuid

from edm.service.interfaces import file_storage as interfaces
from edm.service.models import read as read_models

_TFiles: typing.TypeAlias = dict[uuid.UUID, read_models.FileHydrated]


class MockInMemoryFileStorage(interfaces.FileStorage):
    _common_files: _TFiles = {}

    def __init__(self, files: _TFiles | None = None) -> None:
        self.__files = files

    async def get_by_id(self, file_id: uuid.UUID) -> read_models.FileHydrated | None:
        return self._files.get(file_id)

    async def upload_downloadable(self, file: read_models.FileHydrated) -> interfaces.DownloadUrl:
        self._files[file.guid] = file
        url = f"https://in-memory-storage/{file.guid}"

        return interfaces.DownloadUrl(url)

    @property
    def _files(self) -> _TFiles:
        return self.__files or self._common_files
