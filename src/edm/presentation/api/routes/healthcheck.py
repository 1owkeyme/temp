import fastapi
from fastapi_app import response

from edm.presentation.api.models.schemas import Healthcheck

router = fastapi.APIRouter()


@router.get("/healthcheck", status_code=fastapi.status.HTTP_200_OK)
async def healthcheck() -> response.Response[Healthcheck]:
    """## Получить состояние здоровья сервиса"""
    return response.Response(result=Healthcheck())
