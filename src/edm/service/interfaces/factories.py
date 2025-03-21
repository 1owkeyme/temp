import abc

from edm.service.interfaces import file_storage as file_storage_interfaces
from edm.service.interfaces import package_gateway as package_gateway_interfaces
from edm.service.interfaces import uow as uow_interfaces
from edm.service.interfaces import repositories as repository_interfaces


class FileStorageFactory(abc.ABC):
    @abc.abstractmethod
    def __call__(self) -> file_storage_interfaces.FileStorage:
        pass


class PackageRepositoryFactory(abc.ABC):
    @abc.abstractmethod
    def __call__(self) -> repository_interfaces.PackageRepository:
        pass


class PackageUowFactory(abc.ABC):
    @abc.abstractmethod
    def __call__(self) -> uow_interfaces.PackageUow:
        pass


class OutboxedPackageUowRepositroiesFactory(abc.ABC):
    @abc.abstractmethod
    def __call__(self) -> uow_interfaces.OutboxedPackageUowRepositroies:
        pass


class OutboxedPackageUowFactory(abc.ABC):
    @abc.abstractmethod
    def __call__(self) -> uow_interfaces.OutboxedPackageUow:
        pass


class PackageGatewayFactory(abc.ABC):
    @abc.abstractmethod
    def __call__(self) -> package_gateway_interfaces.PackageGateway:
        pass
