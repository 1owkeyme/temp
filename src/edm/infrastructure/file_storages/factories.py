from edm.infrastructure.file_storages import in_memory_file_storage


class InMemoryFileStorageFactory:
    def __init__(self) -> None:
        pass

    def __call__(self) -> in_memory_file_storage.InMemoryFileStorage:
        return in_memory_file_storage.InMemoryFileStorage()
