import di
from di import dependent

from edm.service.interfaces import factories as factory_interfaces
from tests.mock.file_storages import mock_factories as file_storage_mock_factories
from tests.mock.uow import mock_factories as uow_mock_factories
from tests.mock.repositories import mock_factories as repository_mock_factories


FileStorageFactoryBind = di.bind_by_type(
    dependent.Dependent(file_storage_mock_factories.MockInMemoryFileStorageFactory, scope="request"),
    factory_interfaces.FileStorageFactory,
)

PackageRepositoryFactoryBind = di.bind_by_type(
    dependent.Dependent(repository_mock_factories.MockInMemoryPackageRepositoryFactory, scope="request"),
    factory_interfaces.PackageRepositoryFactory,
)


PackageUowFactoryBind = di.bind_by_type(
    dependent.Dependent(uow_mock_factories.MockInMemoryPackageUowFactory, scope="request"),
    factory_interfaces.PackageUowFactory,
)

OutboxedPackageUowRepositroiesFactoryBind = di.bind_by_type(
    dependent.Dependent(uow_mock_factories.MockInMemoryOutboxedPackageUowRepositroiesFactory, scope="request"),
    factory_interfaces.OutboxedPackageUowRepositroiesFactory,
)


OutboxedPackageUowFactory = di.bind_by_type(
    dependent.Dependent(uow_mock_factories.MockInMemoryOutboxedPackageUowFactory, scope="request"),
    factory_interfaces.OutboxedPackageUowFactory,
)


def di_container_factory() -> di.Container:
    container = di.Container()
    container.bind(FileStorageFactoryBind)
    container.bind(PackageRepositoryFactoryBind)
    container.bind(PackageUowFactoryBind)
    container.bind(OutboxedPackageUowRepositroiesFactoryBind)
    container.bind(OutboxedPackageUowFactory)
    return container
