import typing

from edm.service.interfaces import factories as factory_interfaces
from edm.service.models import commands


async def test_create_package_handler(
    mocked_request_mediator,
    natural_counterparty_factory,
    random_bytes_factory,
) -> None:
    counterparty = natural_counterparty_factory()
    file_names_to_contents: typing.Dict[typing.Text, bytes] = {}
    for i in range(1):
        file_names_to_contents[f"file_{i}.bin"] = random_bytes_factory(size=2)

    command_request = commands.CreatePackage(
        file_names_to_contents=file_names_to_contents,
        counterparty=counterparty,
        for_sign=True,
    )
    package_uow = (await mocked_request_mediator._dispatcher._container.resolve(factory_interfaces.PackageUowFactory))()

    result = await mocked_request_mediator.send(command_request)

    # assert result == expected_result
