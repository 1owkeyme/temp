import abc
import typing
import uuid

import pydantic

from edm.domain import value_objects
from edm.domain.entities import package as package_entities
from edm.service.interfaces.repositories import base


class PackageFilter(pydantic.BaseModel):
    package_status: value_objects.PackageStatus | None = None
    for_sign: pydantic.StrictBool | None = None
    failed: pydantic.StrictBool | None = None
    processed: pydantic.StrictBool | None = None
    counterparty: value_objects.Counterparty | None = None


class PackageRepositoryRead(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, package_id: uuid.UUID) -> package_entities.Package | None:
        pass

    @abc.abstractmethod
    async def get_filtered(self, filter_: PackageFilter) -> typing.List[package_entities.Package]:
        pass


class PackageRepository(base.Repostiory[package_entities.Package], PackageRepositoryRead):
    pass
