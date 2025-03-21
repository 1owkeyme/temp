import functools
import typing

import fastapi

from edm.domain import value_objects

InnNaturalQuery = typing.Annotated[
    typing.Text,
    fastapi.Query(
        pattern=value_objects.counterparty.NATURAL_INN_REGEX,
        description="ИНН ФЛ(12 цифр)",
    ),
]
InnLegalQuery = typing.Annotated[
    typing.Text,
    fastapi.Query(
        pattern=value_objects.counterparty.LEGAL_INN_REGEX,
        description="ИНН ЮЛ(10 цифр)",
    ),
]

KppQuery = typing.Annotated[
    typing.Text,
    fastapi.Query(
        pattern=value_objects.counterparty.KPP_REGEX,
        description="КПП (9 знаков)",
    ),
]


_SnpLengthContraintQuery = functools.partial(
    fastapi.Query,
    min_length=value_objects.snp.MIN_LENGTH,
    max_length=value_objects.snp.MAX_LENGTH,
)

FirstNameQuery = typing.Annotated[
    typing.Text,
    _SnpLengthContraintQuery(
        description="Имя",
    ),
]

SecondNameQuery = typing.Annotated[
    typing.Text,
    _SnpLengthContraintQuery(
        description="Фамилия",
    ),
]

PatronymicQuery = typing.Annotated[
    typing.Text | None,
    _SnpLengthContraintQuery(
        description="Отчество",
    ),
]
