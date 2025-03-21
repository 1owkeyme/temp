from edm.domain import value_objects
from edm.domain.entities import document as document_entities
from edm.domain.entities import package as package_entities
from edm.service.interfaces import factories as factory_interfaces
from edm.service.models import queries, responses


async def test_get_documents_for_counterparty_handler(
    mocked_request_mediator,
    document_factory,
    package_factory,
) -> None:
    existing_document: document_entities.Document = document_factory()
    existing_package_status = value_objects.PackageStatus.CREATED
    existing_package: package_entities.Package = package_factory(
        status=existing_package_status,
        documents={existing_document.guid: existing_document},
    )
    query_request = queries.GetDocumentsForCounterparty(counterparty=existing_package.counterparty)
    expected_result = responses.GetDocuments.from_packages(packages=[existing_package])
    package_uow = (await mocked_request_mediator._dispatcher._container.resolve(factory_interfaces.PackageUowFactory))()
    async with package_uow.transaction() as (uow, package_repository):
        await package_repository.save(existing_package)
        await uow.commit()

    result = await mocked_request_mediator.send(query_request)

    assert len(result.documents) == len(expected_result.documents)
    assert result == expected_result
