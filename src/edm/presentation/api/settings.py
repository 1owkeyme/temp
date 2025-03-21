import typing

import dotenv
import pydantic
import pydantic_settings

dotenv.load_dotenv()


class Api(pydantic_settings.BaseSettings, case_sensitive=True):
    # idempotency
    IDEMPOTENCY_REQUIRE: bool = pydantic.Field(default=False)
    IDEMPOTENCY_METHODS: typing.List[typing.Text] = pydantic.Field(
        default=["POST", "DELETE", "PUT"],
    )
    IDEMPOTENCY_ENFORCE_UUID4: bool = pydantic.Field(default=True)
    # auth
    AUTH_REQUIRE: bool = pydantic.Field(default=False)
    AUTH_KEY_PATTERN: typing.Text = pydantic.Field(default="API_KEY_")
    IGNORE_AUTH_METHODS: typing.List[typing.Text] = pydantic.Field(
        default=[
            "/health",
            "/docs",
            "/redoc",
            "/admin",
            "/openapi.json",
        ],
    )
    # healthcheck
    HEALTHCHECK_PATH: typing.Text = pydantic.Field(default="/healthcheck")
    # telemetry
    TELEMETRY_ENABLE: bool = pydantic.Field(default=False)
    # sentry
    SENTRY_ENABLE: bool = pydantic.Field(default=False)
    model_config = pydantic_settings.SettingsConfigDict(env_prefix="API_")


api_settings = Api()
