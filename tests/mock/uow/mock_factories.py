from edm.service.interfaces import factories as factory_interfaces
from edm.service.interfaces import uow as interfaces
from tests.mock.repositories import mock_in_memory_outboxed_event_repository, mock_in_memory_package_repository
from tests.mock.uow import mock_in_memory_outboxed_package_uow, mock_in_memory_package_uow


class MockInMemoryPackageUowFactory(factory_interfaces.PackageUowFactory):
    def __init__(self, package_repository_factory: factory_interfaces.PackageRepositoryFactory) -> None:
        self._package_repository_factory = package_repository_factory

    def __call__(self) -> interfaces.PackageUow:
        return mock_in_memory_package_uow.MockInMemoryPackageUow(package_repository=self._package_repository_factory())


class MockInMemoryOutboxedPackageUowRepositroiesFactory(factory_interfaces.OutboxedPackageUowRepositroiesFactory):
    def __call__(self) -> interfaces.OutboxedPackageUowRepositroies:
        return interfaces.OutboxedPackageUowRepositroies(
            outboxed_event_repository=mock_in_memory_outboxed_event_repository.MockInMemoryOutboxedEventRepository(),
            package_repository=mock_in_memory_package_repository.MockInMemoryPackageRepository(),
        )


class MockInMemoryOutboxedPackageUowFactory(factory_interfaces.OutboxedPackageUowFactory):
    def __init__(self, repositories_factory: factory_interfaces.OutboxedPackageUowRepositroiesFactory) -> None:
        self._repositories = repositories_factory()

    def __call__(self) -> mock_in_memory_outboxed_package_uow.MockInMemoryOutboxedPackageUow:
        return mock_in_memory_outboxed_package_uow.MockInMemoryOutboxedPackageUow(repositories=self._repositories)
