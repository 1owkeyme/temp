import functools

import pydantic

MIN_LENGTH = 1
MAX_LENGTH = 255


_LengthContraintField = functools.partial(pydantic.Field, min_length=MIN_LENGTH, max_length=MAX_LENGTH)


class SNP(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(frozen=True)

    first_name: pydantic.StrictStr = _LengthContraintField()
    second_name: pydantic.StrictStr = _LengthContraintField()
    patronymic: pydantic.StrictStr | None = _LengthContraintField(default=None)

    def __str__(self) -> str:
        return f"{self.second_name} {self.first_name} {self.patronymic or ''}"
