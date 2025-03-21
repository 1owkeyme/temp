import pydantic
import pytest

from edm.domain.entities import file as file_entities

file_valid_cases = [
    pytest.param("important.pdf", pydantic.AnyUrl("https://s3/important.pdf"), id="file_valid"),
    pytest.param("important.pdf", None, id="file_no_download_url"),
    pytest.param("a" * file_entities.MIN_FILE_NAME_LENGTH, None, id="file_name_short"),
    pytest.param("a" * file_entities.MAX_FILE_NAME_LENGTH, None, id="file_name_long"),
]


file_invalid_cases = [
    pytest.param("", None, id="file_name_empty"),
    pytest.param("important .pdf", None, id="file_name_contains_spaces"),
    pytest.param("a" * (file_entities.MIN_FILE_NAME_LENGTH - 1), None, id="file_name_too_short"),
    pytest.param("a" * (file_entities.MAX_FILE_NAME_LENGTH + 1), None, id="file_name_too_long"),
]
