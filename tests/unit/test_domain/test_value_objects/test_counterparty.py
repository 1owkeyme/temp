import typing

import pydantic
import pytest

from edm.domain import value_objects
from tests.unit.test_domain.test_value_objects import test_counterparty_cases


@pytest.mark.parametrize("inn", test_counterparty_cases.natural_counterparty_valid_cases)
def test_natural_counterparty_valid(inn: typing.Text, snp_factory) -> None:
    snp = snp_factory()
    counterparty = value_objects.counterparty.NaturalCounterparty(inn=inn, snp=snp)

    assert counterparty.inn == inn
    assert counterparty.snp == snp


@pytest.mark.parametrize("inn", test_counterparty_cases.natural_counterparty_invalid_cases)
def test_natural_counterparty_invalid(inn: typing.Text, snp_factory) -> None:
    with pytest.raises(pydantic.ValidationError):
        value_objects.counterparty.NaturalCounterparty(inn=inn, snp=snp_factory())


@pytest.mark.parametrize("inn, kpp", test_counterparty_cases.legal_counterparty_valid_cases)
def test_legal_counterparty_valid(inn: typing.Text, kpp: typing.Text) -> None:
    counterparty = value_objects.counterparty.LegalCounterparty(inn=inn, kpp=kpp)

    assert counterparty.inn == inn
    assert counterparty.kpp == kpp


@pytest.mark.parametrize("inn, kpp", test_counterparty_cases.legal_counterparty_invalid_cases)
def test_legal_counterparty_invalid(inn: typing.Text, kpp: typing.Text) -> None:
    with pytest.raises(pydantic.ValidationError):
        value_objects.counterparty.LegalCounterparty(inn=inn, kpp=kpp)
