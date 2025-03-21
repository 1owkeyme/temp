import abc
import uuid

import pydantic

from edm.service.models import read as read_models


class FileStorageRead(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, file_id: uuid.UUID) -> read_models.FileHydrated | None:
        pass


DownloadUrl = pydantic.AnyUrl


@abc.abstractmethod
class FileStorage(FileStorageRead):
    @abc.abstractmethod
    async def upload_downloadable(self, file: read_models.FileHydrated) -> DownloadUrl:
        pass
