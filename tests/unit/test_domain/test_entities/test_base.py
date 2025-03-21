import uuid

from edm.domain import events as domain_events
from edm.domain.entities import base


def test_aggregate_default() -> None:
    aggregate = base.Aggregate()

    assert len(aggregate.events) == 0


def test_aggregate_register() -> None:
    aggregate = base.Aggregate()
    events = [domain_events.PackageCreated(package_id=uuid.uuid4()) for _ in range(10)]

    for event in events:
        aggregate._register_event(event)

    assert len(aggregate.events) == len(events)
    for registered_event, original_event in zip(aggregate.events, events):
        assert registered_event is original_event
