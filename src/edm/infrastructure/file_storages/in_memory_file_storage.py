import uuid

from edm.service.interfaces import file_storage as interfaces
from edm.service.models import read as read_models


class InMemoryFileStorage(interfaces.FileStorage):
    _storage: dict[uuid.UUID, read_models.FileHydrated] = {}

    async def get_by_id(self, file_id: uuid.UUID) -> read_models.FileHydrated | None:
        return self._storage.get(file_id)

    async def upload_downloadable(self, file: read_models.FileHydrated) -> interfaces.DownloadUrl:
        self._storage[file.guid] = file
        url = f"https://in-memory-storage/{file.guid}"

        return interfaces.DownloadUrl(url)
