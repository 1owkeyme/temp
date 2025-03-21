import datetime
import typing

import cqrs
import fastapi
from fastapi_app import response

from edm.domain import value_objects
from edm.presentation.api import dependencies
from edm.presentation.api.routes.v1 import models
from edm.service.models import queries
from edm.service.models import responses as service_responses

router = fastapi.APIRouter()


@router.get("/natural")
async def get_documents_for_natural(
    inn: models.queries.InnNaturalQuery,
    first_name: models.queries.FirstNameQuery,
    second_name: models.queries.SecondNameQuery,
    patronymic: models.queries.PatronymicQuery = None,
    status: typing.Annotated[
        value_objects.package_status.PackageStatus | None,
        fastapi.Query(description="Фильтрует документы по статусу"),
    ] = None,
    sent_after: typing.Annotated[
        datetime.date | None,
        fastapi.Query(
            description="Фильтрует документы, отправленные **включительно после** указанной даты (YYYY-MM-DD)",
        ),
    ] = None,
    sent_before: typing.Annotated[
        datetime.date | None,
        fastapi.Query(description="Фильтрует документы, отправленные **до** указанной даты (YYYY-MM-DD)"),
    ] = None,
    mediator: cqrs.RequestMediator = fastapi.Depends(dependencies.mediator_factory),
) -> response.Response[service_responses.GetDocuments]:
    """## Получить документы ФЛ"""

    result = await mediator.send(
        queries.GetDocumentsForCounterparty(
            counterparty=value_objects.NaturalCounterparty(
                inn=inn,
                snp=value_objects.SNP(
                    first_name=first_name,
                    second_name=second_name,
                    patronymic=patronymic,
                ),
            ),
        ),
    )

    return response.Response(result=result)


@router.get("/legal")
async def get_documents_for_legal(
    inn: models.queries.InnLegalQuery,
    kpp: models.queries.KppQuery,
    status: typing.Annotated[
        value_objects.package_status.PackageStatus | None,
        fastapi.Query(description="Фильтрует документы по статусу"),
    ] = None,
    sent_after: typing.Annotated[
        datetime.date | None,
        fastapi.Query(
            description="Фильтрует документы, отправленные **включительно после** указанной даты (YYYY-MM-DD)",
        ),
    ] = None,
    sent_before: typing.Annotated[
        datetime.date | None,
        fastapi.Query(description="Фильтрует документы, отправленные **до** указанной даты (YYYY-MM-DD)"),
    ] = None,
    mediator: cqrs.RequestMediator = fastapi.Depends(dependencies.mediator_factory),
) -> response.Response[service_responses.GetDocuments]:
    """## Получить документы ЮЛ"""

    result = await mediator.send(
        queries.GetDocumentsForCounterparty(
            counterparty=value_objects.LegalCounterparty(
                inn=inn,
                kpp=kpp,
            ),
        ),
    )

    return response.Response(result=result)
