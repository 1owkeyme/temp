import pytest

natural_counterparty_valid_cases = [
    pytest.param("123456789012", id="natural_counterparty_valid"),
    pytest.param("000000000000", id="natural_counterparty_valid_inn_all_zeroes"),
]

natural_counterparty_invalid_cases = [
    pytest.param("12345678901", id="natural_counterparty_inn_too_short"),
    pytest.param("1234567890123", id="natural_counterparty_inn_too_long"),
    pytest.param("12345678901A", id="natural_counterparty_inn_contains_letter"),
    pytest.param("123-57890123", id="natural_counterparty_inn_contains_symbol"),
]


legal_counterparty_valid_cases = [
    pytest.param("1234567890", "1234AB567", id="legal_counterparty_valid"),
    pytest.param("0000000000", "9876CD543", id="legal_counterparty_inn_all_zeroes"),
    pytest.param("1234567890", "000000000", id="legal_counterparty_kpp_all_zeroes"),
]


legal_counterparty_invalid_cases = [
    pytest.param("123456789", "1234AB567", id="legal_counterparty_inn_too_short"),
    pytest.param("12345678901", "1234AB567", id="legal_counterparty_inn_too_long"),
    pytest.param("12345678901A", "1234AB567", id="legal_counterparty_inn_contains_letter"),
    pytest.param("12345-789012", "1234AB567", id="legal_counterparty_inn_contains_symbol"),
    pytest.param("1234567890", "1234AB56", id="legal_counterparty_kpp_too_short"),
    pytest.param("1234567890", "1234AB5678", id="legal_counterparty_kpp_too_long"),
    pytest.param("1234567890", "1234ab567", id="legal_counterparty_kpp_contains_lowercase_letters"),
    pytest.param("1234567890", "123-AB567", id="legal_counterparty_kpp_contains_symbol"),
]
