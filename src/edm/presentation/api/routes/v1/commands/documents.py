import asyncio
import datetime
import typing
import uuid

import cqrs
import fastapi
from fastapi_app import response

from edm.domain import value_objects
from edm.presentation.api import dependencies
from edm.presentation.api.routes.v1.models import queries
from edm.service.models import commands
from edm.service.models import responses as service_responses

router = fastapi.APIRouter()


@router.post("/upload/natural")
async def send_documents_to_natural(
    documents: typing.Annotated[
        typing.List[fastapi.UploadFile],
        fastapi.File(description="Документы, которые необходимо выслать контрагенту"),
    ],
    inn: queries.InnNaturalQuery,
    first_name: queries.FirstNameQuery,
    second_name: queries.SecondNameQuery,
    patronymic: queries.PatronymicQuery = None,
    mediator: cqrs.RequestMediator = fastapi.Depends(dependencies.mediator_factory),
) -> response.Response[service_responses.PackageCreated]:
    """## Отправить комплект документов контрагенту ФЛ"""

    file_names_to_contents = {
        document.filename or f"{first_name}-{second_name}-{datetime.datetime.now().isoformat()}": content
        for document, content in zip(documents, await asyncio.gather(*(doc.read() for doc in documents)))
    }
    result = await mediator.send(
        commands.CreatePackage(
            file_names_to_contents=file_names_to_contents,
            counterparty=value_objects.NaturalCounterparty(
                inn=inn,
                snp=value_objects.SNP(
                    first_name=first_name,
                    second_name=second_name,
                    patronymic=patronymic,
                ),
            ),
            for_sign=True,  # TODO: добавить это в тело запроса
        ),
    )
    return response.Response(result=result)


@router.post("/upload/legal")
async def send_documents_to_legal(
    documents: typing.Annotated[
        typing.List[fastapi.UploadFile],
        fastapi.File(description="Документы, которые необходимо выслать контрагенту"),
    ],
    inn: queries.InnLegalQuery,
    kpp: queries.KppQuery,
    mediator: cqrs.RequestMediator = fastapi.Depends(dependencies.mediator_factory),
) -> response.Response[service_responses.PackageCreated]:
    """## Отправить комплект документов контрагенту ЮЛ"""

    file_names_to_contents = {
        document.filename or f"{inn}-{kpp}-{datetime.datetime.now().isoformat()}": content
        for document, content in zip(documents, await asyncio.gather(*(doc.read() for doc in documents)))
    }
    result = await mediator.send(
        commands.CreatePackage(
            file_names_to_contents=file_names_to_contents,
            counterparty=value_objects.LegalCounterparty(
                inn=inn,
                kpp=kpp,
            ),
            for_sign=True,  # TODO: добавить это в тело запроса
        ),
    )
    return response.Response(result=result)


@router.put("/{document_id}/resend")  # TODO: нужен ли...?
def resend_document(document_id: uuid.UUID) -> response.Response[service_responses.ResendDocument]:
    """## Отправить документ повторно"""
    return response.Response(result=service_responses.ResendDocument.model_construct())
