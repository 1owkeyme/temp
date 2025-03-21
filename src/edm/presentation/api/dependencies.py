import functools

from cqrs.requests import bootstrap as request_bootstrap

from edm.service import di, mapping


@functools.lru_cache
def mediator_factory():
    return request_bootstrap.bootstrap(
        di_container=di.container,
        commands_mapper=mapping.init_commands,
        queries_mapper=mapping.init_queries,
        domain_events_mapper=mapping.init_notification_events,
        on_startup=[],
    )
