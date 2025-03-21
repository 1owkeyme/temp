import typing

import cqrs
import pydantic

from edm.domain import value_objects


class CreatePackage(cqrs.Request):
    """Команда на создание пакета."""

    file_names_to_contents: typing.Dict[typing.Text, bytes] = pydantic.Field(exclude=True)
    counterparty: value_objects.Counterparty
    for_sign: pydantic.StrictBool


class QueuePendingPackages(cqrs.Request):
    """Команда на публикацию пакета в очередь отправки."""


class ProcessPackages(cqrs.Request):
    """Команда на начало обработки пакетов, которые дожидаются внешнего результата."""


class ProcessFailedPackages(cqrs.Request):
    """Команда на начало обработки пакетов, которые на предыдущем этапе закончились ошибкой."""
