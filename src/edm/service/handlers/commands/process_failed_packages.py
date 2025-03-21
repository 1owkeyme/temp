import typing

import cqrs
from loguru import logger

from edm.domain import errors as domain_errors
from edm.domain import value_objects
from edm.service.interfaces import factories as factory_interfaces
from edm.service.interfaces import repositories as repository_interfaces
from edm.service.models import commands, responses


class ProcessFailedPackagesHandler(
    cqrs.RequestHandler[commands.ProcessFailedPackages, responses.ProcessFailedPackages],
):
    """
    Обработчик пакетов, процесс обработки которых закончился ошибкой.

    Обработчик максимально простой - переводит пакет в предыдущий статус для повторной обработки.
    """

    def __init__(
        self,
        outboxed_package_uow_factory: factory_interfaces.OutboxedPackageUowFactory,  # TODO: decide whether it is required to have factory here
    ) -> None:
        self._outboxed_package_uow = outboxed_package_uow_factory()

    @property
    def events(self) -> typing.List[cqrs.Event]:
        return []

    async def handle(self, request: commands.ProcessFailedPackages) -> responses.ProcessFailedPackages:
        package_filter = repository_interfaces.package.PackageFilter(
            failed=True,
            processed=False,
        )
        async with self._outboxed_package_uow.transaction() as (outboxed_package_uow, repositories):
            packages = await repositories.package_repository.get_filtered(package_filter)

            for package in packages:
                try:
                    match package.status:
                        case value_objects.PackageStatus.QUEUED:
                            package.recover_to_queued()
                        case value_objects.PackageStatus.SIGNED:
                            package.recover_to_signed()
                except domain_errors.AggregateExpired as exc:
                    logger.error(str(exc))
                except domain_errors.InvalidTransition as exc:
                    package.mark_as_failed(reason=str(exc), should_try_again=False)

                await repositories.package_repository.save(package)
                await outboxed_package_uow.commit()

        return responses.ProcessFailedPackages.model_construct()
