import asyncio
import datetime
import random
import string
import typing
import uuid

import faker
import fastapi_app
import httpx
import pydantic
import pytest

from edm import settings
from edm.domain import value_objects
from edm.domain.entities import document as document_entities
from edm.domain.entities import file as file_entities
from edm.domain.entities import package as package_entities
from edm.presentation import dependencies as global_dependencies
from edm.presentation.api import routes
from edm.presentation.api import settings as api_settings
from edm.presentation.api.main import app as api_app
from tests.mock import mock_dependencies


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope="function")
def mock_app():
    return fastapi_app.create(
        debug=True,
        title=settings.app_settings.NAME,
        version=settings.app_settings.VERSION,
        description='Тарификатор продукта "Виртуальный хостинг"',
        env_title=settings.app_settings.ENV,
        query_routers=(routes.queries_routers,),
        command_routers=[],
        middlewares=[],
        startup_tasks=[],
        shutdown_tasks=[],
        global_dependencies=[],
        idempotency_require=True,
        idempotency_backed=None,
        idempotency_methods=api_settings.api_settings.IDEMPOTENCY_METHODS,
        auth_require=False,
        exception_handlers=[],
    )


@pytest.fixture(scope="function")
def mock_api():
    api_app.dependency_overrides[global_dependencies.request_mediator_factory] = (
        mock_dependencies.mock_request_mediator_factory
    )
    return api_app


@pytest.fixture(scope="function")
async def mocked_api_client(
    mock_api,
) -> typing.AsyncGenerator[httpx.AsyncClient, typing.Any]:
    """Асинхронный http клиент"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(mock_api),
        base_url="http://test-api/api",
    ) as client:
        yield client


@pytest.fixture(scope="session")
def fake() -> faker.Faker:
    return faker.Faker()


@pytest.fixture(scope="session")
def snp_factory(fake: faker.Faker):
    def _create_snp():
        return value_objects.SNP(
            first_name=fake.first_name(),
            second_name=fake.last_name(),
            patronymic=fake.first_name(),
        )

    return _create_snp


@pytest.fixture(scope="session")
def natural_counterparty_factory(snp_factory):
    def _create_snp():
        inn = "".join(random.choices(string.digits, k=12))
        return value_objects.counterparty.NaturalCounterparty(inn=inn, snp=snp_factory())

    return _create_snp


@pytest.fixture(scope="session")
def file_factory(fake: faker.Faker):
    def _create_file():
        return file_entities.File(name=fake.file_name(extension="pdf"), download_url=pydantic.AnyUrl(fake.url()))

    return _create_file


@pytest.fixture(scope="session")
def document_factory(file_factory):
    def _create_document():
        return document_entities.Document(file=file_factory(), file_signed=None, external_file_id=None)

    return _create_document


@pytest.fixture(scope="session")
def package_factory(
    natural_counterparty_factory,
    document_factory,
) -> typing.Callable[..., package_entities.Package]:
    def _create_package(
        *,
        package_id: uuid.UUID | None = None,
        for_sign=True,
        status=value_objects.PackageStatus.DRAFT,
        expired=False,
        failure_status=value_objects.FailureStatus.NoFailure,
        failure_reason="",
        documents: typing.Dict[uuid.UUID, document_entities.Document] | None = None,
    ) -> package_entities.Package:
        if package_id is None:
            package_id = uuid.uuid4()

        if documents is None:
            document: document_entities.Document = document_factory()
            documents = {document.guid: document}

        package = package_entities.Package(
            guid=package_id,
            counterparty=natural_counterparty_factory(),
            for_sign=for_sign,
            documents=documents,
            status=status,
            expiration_date=datetime.datetime.now() - datetime.timedelta(days=1) if expired else datetime.datetime.max,
            failure_status=failure_status,
            failure_reason=failure_reason,
        )
        return package

    return _create_package


@pytest.fixture(scope="session")
def random_bytes_factory(fake: faker.Faker) -> typing.Callable[..., bytes]:
    def _create_random_bytes(size: int = 1024) -> bytes:
        return fake.binary(length=size)

    return _create_random_bytes
