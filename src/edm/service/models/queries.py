import cqrs

from edm.domain import value_objects


class GetDocumentsForCounterparty(cqrs.Request):
    """Команда на получение всех документов контрагента."""

    counterparty: value_objects.Counterparty
