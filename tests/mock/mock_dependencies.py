import functools

import cqrs
from cqrs.events import bootstrap as event_bootstrap
from cqrs.requests import bootstrap as request_bootstrap
import di
from edm.service import mapping


@functools.lru_cache
def mock_request_mediator_factory(di_container: di.Container) -> cqrs.RequestMediator:
    return request_bootstrap.bootstrap(
        di_container=di_container,
        commands_mapper=mapping.init_commands,
        queries_mapper=mapping.init_queries,
        domain_events_mapper=mapping.init_domain_events,
        on_startup=[],
    )


@functools.lru_cache
def mock_event_mediator_factory(di_container: di.Container) -> cqrs.EventMediator:
    return event_bootstrap.bootstrap(
        di_container=di_container,
        events_mapper=mapping.init_notification_events,
        on_startup=[],
    )
