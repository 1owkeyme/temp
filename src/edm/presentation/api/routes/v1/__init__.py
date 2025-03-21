import fastapi

from edm.presentation.api.routes.v1.commands import documents as documents_commands
from edm.presentation.api.routes.v1.queries import documents as documents_queries

commands_routers = fastapi.APIRouter()
commands_routers.include_router(documents_commands.router, prefix="/documents", tags=["Документы"])

queries_routers = fastapi.APIRouter()
queries_routers.include_router(documents_queries.router, prefix="/documents", tags=["Документы"])
