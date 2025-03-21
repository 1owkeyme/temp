# TODO: возможно файл di должен находится в инфрастуктурном слое

import di
from di import dependent

from edm.infrastructure.file_storages import factories as file_storage_factories
from edm.infrastructure.uow import factories as uow_factories
from edm.service.interfaces import factories as factory_interfaces

container = di.Container()

__all__ = ["container"]


FileStorageFactoryBind = di.bind_by_type(
    dependent.Dependent(file_storage_factories.InMemoryFileStorageFactory, scope="request"),
    factory_interfaces.FileStorageFactory,
)

PackageUowFactoryBind = di.bind_by_type(
    dependent.Dependent(
        uow_factories.InMemoryPackageUowFactory,
        scope="request",
    ),  # TODO: решить нужна ли фактори
    factory_interfaces.PackageUowFactory,
)

OutboxedPackageUowRepositroiesFactoryBind = di.bind_by_type(
    dependent.Dependent(uow_factories.InMemoryOutboxedPackageUowRepositroiesFactory, scope="request"),
    factory_interfaces.OutboxedPackageUowRepositroiesFactory,
)


OutboxedPackageUowFactory = di.bind_by_type(
    dependent.Dependent(
        uow_factories.InMemoryOutboxedPackageUowFactory,
        scope="request",
    ),  # TODO: решить нужна ли фактори
    factory_interfaces.OutboxedPackageUowFactory,
)

container.bind(FileStorageFactoryBind)
container.bind(PackageUowFactoryBind)
container.bind(OutboxedPackageUowRepositroiesFactoryBind)
container.bind(OutboxedPackageUowFactory)
