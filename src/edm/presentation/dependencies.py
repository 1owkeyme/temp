import functools

import cqrs
from cqrs.events import bootstrap as event_bootstrap
from cqrs.requests import bootstrap as request_bootstrap

from edm.service import di, mapping


@functools.lru_cache
def request_mediator_factory() -> cqrs.RequestMediator:
    return request_bootstrap.bootstrap(
        di_container=di.container,
        commands_mapper=mapping.init_commands,
        queries_mapper=mapping.init_queries,
        domain_events_mapper=mapping.init_domain_events,
        on_startup=[],
    )


@functools.lru_cache
def event_mediator_factory() -> cqrs.EventMediator:
    return event_bootstrap.bootstrap(
        di_container=di.container,
        events_mapper=mapping.init_notification_events,
        on_startup=[],
    )
