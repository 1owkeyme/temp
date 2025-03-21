import logging
from logging import config

import fastapi_app
from fastapi_app import logging as fastapi_logging

from edm import settings
from edm.presentation.api import routes
from edm.presentation.api import settings as api_settings

log_config = fastapi_logging.generate_log_config(
    logging_level=settings.logging_settings.LEVEL,
    serialize=settings.logging_settings.SERIALIZE,
    app_name=settings.app_settings.NAME,
    app_version=settings.app_settings.VERSION,
)

config.dictConfig(log_config)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

app = fastapi_app.create(
    title=settings.app_settings.NAME,
    version=settings.app_settings.VERSION,
    description="Доставка документов контрагентам через системы ЭДО",
    env_title=settings.app_settings.ENV,
    query_routers=[routes.queries_routers],
    command_routers=[routes.commands_routers],
    middlewares=[],
    startup_tasks=[],
    shutdown_tasks=[],
    global_dependencies=[],
    idempotency_require=True,
    idempotency_backed=None,
    idempotency_methods=api_settings.api_settings.IDEMPOTENCY_METHODS,
    auth_require=False,
    exception_handlers=[],  # TODO:
)
