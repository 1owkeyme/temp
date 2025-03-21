from edm.infrastructure.repositories import in_memory_outboxed_event_repository, in_memory_package_repository


class InMemoryPackageRepositoryFactory:
    def __init__(self) -> None:
        pass

    def __call__(self) -> in_memory_package_repository.InMemoryPackageRepository:
        return in_memory_package_repository.InMemoryPackageRepository()


class InMemoryOutboxedEventRepositoryFactory:
    def __init__(self) -> None:
        pass

    def __call__(self) -> in_memory_outboxed_event_repository.InMemoryOutboxedEventRepository:
        return in_memory_outboxed_event_repository.InMemoryOutboxedEventRepository()
