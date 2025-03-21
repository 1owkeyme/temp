import typing
import uuid

from edm.domain import value_objects
from edm.domain.entities import package as package_entities
from edm.service.interfaces import repositories as interfaces


class InMemoryPackageRepository(interfaces.PackageRepository):
    _packages: dict[uuid.UUID, package_entities.Package] = {}

    async def get_by_id(self, package_id: uuid.UUID) -> package_entities.Package | None:
        return self._packages.get(package_id)

    async def get_filtered(self, filter_: interfaces.package.PackageFilter) -> typing.List[package_entities.Package]:
        return [
            package
            for package in self._packages.values()
            if (
                (filter_.package_status is None or package.status == filter_.package_status)
                and (filter_.for_sign is None or package.for_sign == filter_.for_sign)
                and (
                    filter_.failed is None
                    or (package.failure_status != value_objects.FailureStatus.NoFailure) == filter_.failed
                )
                and (filter_.processed is None or package.processed == filter_.processed)
            )
        ]

    async def commit(self) -> None:
        return

    async def rollback(self) -> None:
        return

    async def _save(self, package: package_entities.Package) -> None:
        self._packages[package.guid] = package
