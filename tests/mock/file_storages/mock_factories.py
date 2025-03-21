from tests.mock.file_storages import mock_in_memory_file_storage


class MockInMemoryFileStorageFactory:
    def __init__(self) -> None:
        pass

    def __call__(self) -> mock_in_memory_file_storage.MockInMemoryFileStorage:
        return mock_in_memory_file_storage.MockInMemoryFileStorage()
