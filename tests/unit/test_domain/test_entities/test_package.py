import datetime
import uuid

import pytest
from _pytest.mark.structures import ParameterSet
from freezegun import freeze_time

from edm.domain import errors, value_objects
from edm.domain.entities import document as document_entities
from edm.domain.entities import file as file_entities
from edm.domain.entities import package as package_entities
from tests.unit.test_domain.test_entities import test_package_cases


def test_package_default(natural_counterparty_factory) -> None:
    now = datetime.datetime.now()
    expiration_date = now + datetime.timedelta(days=365)

    with freeze_time(now):
        package = package_entities.Package(
            counterparty=natural_counterparty_factory(),
            for_sign=False,
            documents={},
        )

        assert package.status is value_objects.PackageStatus.DRAFT
        assert package.failure_status is value_objects.FailureStatus.NoFailure
        assert package.expiration_date == expiration_date


@pytest.mark.parametrize(
    "package_id,reason,should_try_again,expected_failure_status,expected_failure_reason,processed,expected_events",
    test_package_cases.mark_as_failed_cases,
)
def test_package_mark_as_failed(
    package_id,
    reason,
    should_try_again,
    expected_failure_status,
    expected_failure_reason,
    processed: ParameterSet,
    expected_events,
    package_factory,
) -> None:
    package: package_entities.Package = package_factory(package_id=package_id)

    package.mark_as_failed(reason, should_try_again)

    assert package.guid == package_id
    assert package.failure_status == expected_failure_status
    assert package.failure_reason == expected_failure_reason
    assert package.events == expected_events
    assert package.processed == processed


def test_package_set_external_file_id_for_document(document_factory, package_factory) -> None:
    document: document_entities.Document = document_factory()
    package: package_entities.Package = package_factory(documents={document.guid: document})
    external_file_id = "external_file_id_123"

    package.set_external_file_id_for_document(document.guid, external_file_id)

    assert package.documents[document.guid].external_file_id == external_file_id


def test_package_set_external_file_id_for_unknown_document(document_factory, package_factory) -> None:
    document: document_entities.Document = document_factory()
    package: package_entities.Package = package_factory(documents={document.guid: document})
    external_file_id = "external_file_id_123"
    unknown_document_id = uuid.uuid4()

    with pytest.raises(errors.InvalidEntityId, match=str(unknown_document_id)):
        package.set_external_file_id_for_document(unknown_document_id, external_file_id)

    assert package.documents[document.guid].external_file_id != external_file_id


def test_package_set_signed_file_for_document(
    file_factory,
    document_factory,
    package_factory,
) -> None:
    file_signed: file_entities.File = file_factory()
    document: document_entities.Document = document_factory()
    package: package_entities.Package = package_factory(documents={document.guid: document})

    package.set_signed_file_for_document(document.guid, file_signed)

    assert package.documents[document.guid].file_signed == file_signed


def test_package_set_signed_file_for_unknown_document(
    file_factory,
    document_factory,
    package_factory,
) -> None:
    file_signed: file_entities.File = file_factory()
    document: document_entities.Document = document_factory()
    package: package_entities.Package = package_factory(documents={document.guid: document})
    unknown_document_id = uuid.uuid4()

    with pytest.raises(errors.InvalidEntityId, match=str(unknown_document_id)):
        package.set_signed_file_for_document(unknown_document_id, file_signed)

    assert package.documents[document.guid].file_signed != file_signed


class TestPackageStatusTransitions:
    @pytest.mark.parametrize(
        "package_id,start_status,for_sign,failure_status,expectation_context,expected_status,processed,expected_events",
        test_package_cases.mark_as_created_cases,
    )
    def test_mark_as_created(
        self,
        package_id,
        start_status,
        for_sign,
        failure_status,
        expectation_context,
        expected_status,
        processed,
        expected_events,
        package_factory,
    ) -> None:
        package: package_entities.Package = package_factory(
            package_id=package_id,
            status=start_status,
            for_sign=for_sign,
            failure_status=failure_status,
        )

        with expectation_context:
            package.mark_as_created()

        assert package.guid == package_id
        assert package.status == expected_status
        assert package.events == expected_events
        assert package.processed == processed

    @pytest.mark.parametrize(
        "package_id,start_status,for_sign,failure_status,expectation_context,expected_status,processed,expected_events",
        test_package_cases.mark_as_queued_cases,
    )
    def test_mark_as_queued(
        self,
        package_id,
        start_status,
        for_sign,
        failure_status,
        expectation_context,
        expected_status,
        processed,
        expected_events,
        package_factory,
    ) -> None:
        package: package_entities.Package = package_factory(
            package_id=package_id,
            status=start_status,
            for_sign=for_sign,
            failure_status=failure_status,
        )

        with expectation_context:
            package.mark_as_queued()

        assert package.guid == package_id
        assert package.status == expected_status
        assert package.events == expected_events
        assert package.processed == processed

    @pytest.mark.parametrize(
        "package_id,start_status,for_sign,failure_status,expectation_context,expected_status,processed,expected_events",
        test_package_cases.mark_as_sent_cases,
    )
    def test_mark_as_sent(
        self,
        package_id,
        start_status,
        for_sign,
        failure_status,
        expectation_context,
        expected_status,
        processed,
        expected_events,
        package_factory,
    ) -> None:
        package: package_entities.Package = package_factory(
            package_id=package_id,
            status=start_status,
            for_sign=for_sign,
            failure_status=failure_status,
        )

        with expectation_context:
            package.mark_as_sent()

        assert package.guid == package_id
        assert package.status == expected_status
        assert package.events == expected_events
        assert package.processed == processed

    @pytest.mark.parametrize(
        "package_id,start_status,for_sign,failure_status,expectation_context,expected_status,processed,expected_events",
        test_package_cases.mark_as_signed_cases,
    )
    def test_mark_as_signed(
        self,
        package_id,
        start_status,
        for_sign,
        failure_status,
        expectation_context,
        expected_status,
        processed,
        expected_events,
        package_factory,
    ) -> None:
        package: package_entities.Package = package_factory(
            package_id=package_id,
            status=start_status,
            for_sign=for_sign,
            failure_status=failure_status,
        )

        with expectation_context:
            package.mark_as_signed()

        assert package.guid == package_id
        assert package.status == expected_status
        assert package.events == expected_events
        assert package.processed == processed

    @pytest.mark.parametrize(
        "package_id,start_status,for_sign,failure_status,expectation_context,expected_status,processed,expected_events",
        test_package_cases.mark_as_signed_downloaded_cases,
    )
    def test_mark_as_signed_downloaded(
        self,
        package_id,
        start_status,
        for_sign,
        failure_status,
        expectation_context,
        expected_status,
        processed,
        expected_events,
        package_factory,
    ) -> None:
        package: package_entities.Package = package_factory(
            package_id=package_id,
            status=start_status,
            for_sign=for_sign,
            failure_status=failure_status,
        )

        with expectation_context:
            package.mark_as_signed_downloaded()

        assert package.guid == package_id
        assert package.status == expected_status
        assert package.events == expected_events
        assert package.processed == processed


class TestPackageStatusRecovers:
    @pytest.mark.parametrize(
        "package_id,start_status,failure_status,failure_reason,expired,expectation_context,expected_status,expected_failure_status,expected_failure_reason,expected_events",
        test_package_cases.recover_to_queued_cases,
    )
    def test_recover_to_queued(
        self,
        package_id,
        start_status,
        failure_status,
        failure_reason,
        expired,
        expectation_context,
        expected_status,
        expected_failure_status,
        expected_failure_reason,
        expected_events,
        package_factory,
    ) -> None:
        package: package_entities.Package = package_factory(
            package_id=package_id,
            status=start_status,
            failure_status=failure_status,
            failure_reason=failure_reason,
            expired=expired,
        )

        with expectation_context:
            package.recover_to_queued()

        assert package.guid == package_id
        assert package.status == expected_status
        assert package.failure_status == expected_failure_status
        assert package.failure_reason == expected_failure_reason
        assert package.events == expected_events

    @pytest.mark.parametrize(
        "package_id,start_status,failure_status,failure_reason,expired,expectation_context,expected_status,expected_failure_status,expected_failure_reason,expected_events",
        test_package_cases.recover_to_signed_cases,
    )
    def test_recover_to_signed(
        self,
        package_id,
        start_status,
        failure_status,
        failure_reason,
        expired,
        expectation_context,
        expected_status,
        expected_failure_status,
        expected_failure_reason,
        expected_events,
        package_factory,
    ) -> None:
        package: package_entities.Package = package_factory(
            package_id=package_id,
            status=start_status,
            failure_status=failure_status,
            failure_reason=failure_reason,
            expired=expired,
        )

        with expectation_context:
            package.recover_to_signed()

        assert package.guid == package_id
        assert package.status == expected_status
        assert package.failure_status == expected_failure_status
        assert package.failure_reason == expected_failure_reason
        assert package.events == expected_events
