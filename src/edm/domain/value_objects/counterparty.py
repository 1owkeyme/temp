import abc

import pydantic

from edm.domain.value_objects import snp

NATURAL_INN_REGEX = r"^\d{12}$"
LEGAL_INN_REGEX = r"^\d{10}$"
KPP_REGEX = r"^(\d{4}[\dA-Z]{2}\d{3})$"


class Counterparty(abc.ABC, pydantic.BaseModel):
    model_config = pydantic.ConfigDict(frozen=True)

    @abc.abstractmethod
    def __str__(self) -> str:
        pass


class NaturalCounterparty(Counterparty):
    inn: pydantic.StrictStr = pydantic.Field(pattern=NATURAL_INN_REGEX)
    snp: snp.SNP

    def __str__(self) -> str:
        return str(self.snp)


class LegalCounterparty(Counterparty):
    inn: pydantic.StrictStr = pydantic.Field(pattern=LEGAL_INN_REGEX)
    kpp: pydantic.StrictStr = pydantic.Field(pattern=KPP_REGEX)

    def __str__(self) -> str:
        return f"Inn: {self.inn}. Kpp: {self.kpp}"
