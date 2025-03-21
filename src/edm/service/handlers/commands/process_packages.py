import typing

import cqrs
from loguru import logger

from edm.domain import errors as domain_errors
from edm.domain import value_objects
from edm.service.interfaces import factories as factory_interfaces
from edm.service.interfaces import repositories as repository_interfaces
from edm.service.models import commands, responses


class ProcessPackagesHandler(cqrs.RequestHandler[commands.ProcessPackages, responses.ProcessPackages]):
    def __init__(
        self,
        outboxed_package_uow_factory: factory_interfaces.OutboxedPackageUowFactory,  # TODO: возможно тут не нужна фактори
        package_gateway_factory: factory_interfaces.PackageGatewayFactory,
    ) -> None:
        self._outboxed_package_uow = outboxed_package_uow_factory()
        self._package_gateway = package_gateway_factory()

    @property
    def events(self) -> typing.List[cqrs.Event]:
        return []

    async def handle(self, request: commands.ProcessPackages) -> responses.ProcessPackages:
        await self.handle_waiting_for_sign()

        return responses.ProcessPackages.model_construct()

    async def handle_waiting_for_sign(self) -> None:
        package_filter = repository_interfaces.package.PackageFilter(
            package_status=value_objects.PackageStatus.SENT,
            for_sign=True,
        )
        async with self._outboxed_package_uow.transaction() as (outboxed_package_uow, repositories):
            packages = await repositories.package_repository.get_filtered(package_filter)

            for package in packages:
                if not self._package_gateway.is_package_signed(package):
                    logger.info(f"Package `{package.guid}` is not yet signed")
                    continue

                try:
                    package.mark_as_signed()
                except domain_errors.InvalidTransition as exc:
                    package.mark_as_failed(reason=str(exc), should_try_again=False)

                await repositories.package_repository.save(package)
                await outboxed_package_uow.commit()
