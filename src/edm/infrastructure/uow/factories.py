from edm.infrastructure.repositories import in_memory_outboxed_event_repository, in_memory_package_repository
from edm.infrastructure.uow import in_memory_outboxed_package_uow, in_memory_package_uow
from edm.service.interfaces import factories as factory_interfaces
from edm.service.interfaces import uow as interfaces


class InMemoryPackageUowFactory(factory_interfaces.PackageUowFactory):
    def __call__(self) -> interfaces.PackageUow:
        return in_memory_package_uow.InMemoryPackageUow(
            package_repository=in_memory_package_repository.InMemoryPackageRepository(),
        )


class InMemoryOutboxedPackageUowRepositroiesFactory(factory_interfaces.OutboxedPackageUowRepositroiesFactory):
    def __call__(self) -> interfaces.OutboxedPackageUowRepositroies:
        return interfaces.OutboxedPackageUowRepositroies(
            outboxed_event_repository=in_memory_outboxed_event_repository.InMemoryOutboxedEventRepository(),
            package_repository=in_memory_package_repository.InMemoryPackageRepository(),
        )


class InMemoryOutboxedPackageUowFactory(factory_interfaces.OutboxedPackageUowFactory):
    def __init__(self, repositories_factory: factory_interfaces.OutboxedPackageUowRepositroiesFactory) -> None:
        self._repositories = repositories_factory()

    def __call__(self) -> in_memory_outboxed_package_uow.InMemoryOutboxedPackageUow:
        return in_memory_outboxed_package_uow.InMemoryOutboxedPackageUow(repositories=self._repositories)
