import typing

import pydantic
import pytest

from edm.domain import value_objects
from tests.unit.test_domain.test_value_objects import test_snp_cases


@pytest.mark.parametrize("first_name, second_name, patronymic", test_snp_cases.snp_valid_cases)
def test_snp_valid(first_name: typing.Text, second_name: typing.Text, patronymic: typing.Text | None) -> None:
    model = value_objects.SNP(first_name=first_name, second_name=second_name, patronymic=patronymic)

    assert model.first_name == first_name
    assert model.second_name == second_name
    assert model.patronymic == patronymic


@pytest.mark.parametrize("first_name, second_name, patronymic", test_snp_cases.snp_invalid_cases)
def test_snp_invalid(first_name: typing.Text, second_name: typing.Text, patronymic: typing.Text) -> None:
    with pytest.raises(pydantic.ValidationError):
        value_objects.SNP(first_name=first_name, second_name=second_name, patronymic=patronymic)
