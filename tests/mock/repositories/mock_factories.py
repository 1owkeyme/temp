from tests.mock.repositories import mock_in_memory_package_repository


class MockInMemoryPackageRepositoryFactory:
    def __init__(self) -> None:
        self._only_in_memory_package_repository = mock_in_memory_package_repository.MockInMemoryPackageRepository(
            packages={}
        )

    def __call__(self) -> mock_in_memory_package_repository.MockInMemoryPackageRepository:
        return self._only_in_memory_package_repository
