import pytest

from edm.domain import value_objects

snp_valid_cases = [
    pytest.param("John", "Doe", "Ivanovich", id="snp_valid"),
    pytest.param("Alice", "Smith", None, id="snp_no_patronymic"),
    pytest.param("a" * value_objects.snp.MIN_LENGTH, "Doe", "Ivanovich", id="snp_first_name_short"),
    pytest.param("a" * value_objects.snp.MAX_LENGTH, "Doe", "Ivanovich", id="snp_first_name_long"),
    pytest.param("John", "a" * value_objects.snp.MIN_LENGTH, "Ivanovich", id="snp_second_name_short"),
    pytest.param("John", "a" * value_objects.snp.MAX_LENGTH, "Ivanovich", id="snp_second_name_long"),
    pytest.param("John", "Doe", "a" * value_objects.snp.MIN_LENGTH, id="snp_patronymic_short"),
    pytest.param("John", "Doe", "a" * value_objects.snp.MAX_LENGTH, id="snp_patronymic_long"),
]

snp_invalid_cases = [
    pytest.param("", "Doe", "Ivanovich", id="snp_first_name_empty"),
    pytest.param("John", "", "Ivanovich", id="snp_second_name_empty"),
    pytest.param("a" * (value_objects.snp.MIN_LENGTH - 1), "Doe", "Ivanovich", id="snp_first_name_too_short"),
    pytest.param("a" * (value_objects.snp.MAX_LENGTH + 1), "Doe", "Ivanovich", id="snp_first_name_too_long"),
    pytest.param("John", "a" * (value_objects.snp.MIN_LENGTH - 1), "Ivanovich", id="snp_second_name_too_short"),
    pytest.param("John", "a" * (value_objects.snp.MAX_LENGTH + 1), "Ivanovich", id="snp_second_name_too_long"),
    pytest.param("John", "Doe", "a" * (value_objects.snp.MIN_LENGTH - 1), id="snp_patronymic_too_short"),
    pytest.param("John", "Doe", "a" * (value_objects.snp.MAX_LENGTH + 1), id="snp_patronymic_too_long"),
]
