import importlib
import typing

import dotenv
import pydantic
import pydantic_settings

dotenv.load_dotenv()


class Logging(pydantic_settings.BaseSettings, case_sensitive=True):
    """Logging config"""

    LEVEL: typing.Literal["DEBUG", "INFO"] = pydantic.Field(default="DEBUG")
    COLORIZE: bool = pydantic.Field(default=True)
    SERIALIZE: bool = pydantic.Field(default=False)

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="LOGGING_")


class App(pydantic_settings.BaseSettings, case_sensitive=True):
    NAME: typing.Text = pydantic.Field(default="billing_edm")
    ENV: typing.Literal["local", "dev", "prod"] = pydantic.Field(default="local")

    @property
    def VERSION(self) -> typing.Text:
        return importlib.metadata.version(self.NAME)  # type: ignore

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="APP_")


app_settings = App()
logging_settings = Logging()
