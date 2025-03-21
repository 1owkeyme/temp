import typing

import pydantic
import pytest

from edm.domain.entities import file as file_entities
from tests.unit.test_domain.test_entities import test_file_cases


@pytest.mark.parametrize("name, download_url", test_file_cases.file_valid_cases)
def test_file_valid(name: typing.Text, download_url: pydantic.AnyUrl | None) -> None:
    file = file_entities.File(name=name, download_url=download_url)

    assert file.name == name
    assert file.download_url == download_url


@pytest.mark.parametrize("name, download_url", test_file_cases.file_invalid_cases)
def test_file_invalid(name: typing.Text, download_url: pydantic.AnyUrl | None) -> None:
    with pytest.raises(pydantic.ValidationError):
        file_entities.File(name=name, download_url=download_url)


def test_file_set_download_url() -> None:
    file = file_entities.File(name="important.pdf", download_url=None)
    download_url = pydantic.AnyUrl("http://s3/important.pdf")

    file.set_download_url(pydantic.AnyUrl(download_url))

    assert file.download_url == download_url
