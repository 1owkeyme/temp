import fastapi
from fastapi_app import response

from edm import settings
from edm.presentation.api.models import schemas

router = fastapi.APIRouter()


@router.get("/version")
def get_version() -> response.Response[schemas.VersionEmbed]:
    """## Получить версию сервиса"""
    return response.Response(result=schemas.VersionEmbed.model_construct(version=settings.app_settings.VERSION))
