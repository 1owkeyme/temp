import typing

import cqrs

from edm.service.interfaces import factories as factory_interfaces
from edm.service.interfaces import repositories as repository_interfaces
from edm.service.models import queries, responses


class GetDocumentsForCounterpartyHandler(
    cqrs.RequestHandler[queries.GetDocumentsForCounterparty, responses.GetDocuments],
):
    """Обработчик запроса на чтение всех документов для конкретного ФЛ."""

    def __init__(
        self,
        file_storage_factory: factory_interfaces.FileStorageFactory,  # TODO: возможно тут не нужна фактори
        package_uow_factory: factory_interfaces.PackageUowFactory,
    ) -> None:
        self._file_storage = file_storage_factory()
        self._package_uow = package_uow_factory()

    @property
    def events(self) -> typing.List[cqrs.Event]:
        return []

    async def handle(self, request: queries.GetDocumentsForCounterparty) -> responses.GetDocuments:
        package_filter = repository_interfaces.package.PackageFilter(counterparty=request.counterparty)
        async with self._package_uow.transaction() as (_, repo):
            packages = await repo.get_filtered(package_filter)

        return responses.GetDocuments.from_packages(packages)
