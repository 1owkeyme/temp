import fastapi

from edm.presentation.api.routes import healthcheck, version
from edm.presentation.api.routes.v1 import commands_routers as commands_routers_v1
from edm.presentation.api.routes.v1 import queries_routers as queries_routers_v1

__all__ = ("queries_routers", "commands_routers")

queries_routers = fastapi.APIRouter(prefix="/api")
commands_routers = fastapi.APIRouter(prefix="/api")

queries_routers.include_router(version.router, tags=["Сервис"])
queries_routers.include_router(healthcheck.router, tags=["Сервис"])

queries_routers.include_router(queries_routers_v1, prefix="/v1")

commands_routers.include_router(commands_routers_v1, prefix="/v1")
