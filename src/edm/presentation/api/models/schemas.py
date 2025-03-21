import typing

import pydantic


class Check(pydantic.BaseModel):
    name: typing.Text = pydantic.Field(description="Название проверки")
    healthy: bool = pydantic.Field(default=True)
    error: typing.Text = pydantic.Field(default="", description="Сообщение об ошибке")

    def __bool__(self):
        return self.healthy


class Healthcheck(pydantic.BaseModel):
    checks: typing.List[Check] = pydantic.Field(default_factory=list, description="Список проверок")

    @pydantic.computed_field()
    def healthy(self) -> bool:
        return all(self.checks)


class VersionEmbed(pydantic.BaseModel):
    version: typing.Text
