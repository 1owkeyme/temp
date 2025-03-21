from edm.domain.entities import document as document_entities


def test_document_set_signed_file(file_factory) -> None:
    document = document_entities.Document(file=file_factory(), external_file_id=None, file_signed=None)
    signed_file = file_factory()

    document.set_file_signed(signed_file)

    assert document.file_signed


def test_document_set_external_file_id(file_factory) -> None:
    document = document_entities.Document(file=file_factory(), external_file_id=None, file_signed=None)
    external_file_id = "0123456789ABCDEF"

    document.set_external_file_id(external_file_id)

    assert document.external_file_id == external_file_id
