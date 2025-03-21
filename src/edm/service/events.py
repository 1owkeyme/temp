import typing

import cqrs

from edm.domain import events as domain_events


def get_service_event_name(event: typing.Type[domain_events.DeferredDomainEvent]) -> str:
    return event.__name__


cqrs.OutboxedEventMap.register(
    get_service_event_name(domain_events.PackageCreated),
    cqrs.NotificationEvent[domain_events.PackageCreated],
)


cqrs.OutboxedEventMap.register(
    get_service_event_name(domain_events.PackageQueued),
    cqrs.NotificationEvent[domain_events.PackageQueued],
)


cqrs.OutboxedEventMap.register(
    get_service_event_name(domain_events.PackageSigned),
    cqrs.NotificationEvent[domain_events.PackageSigned],
)


cqrs.OutboxedEventMap.register(
    get_service_event_name(domain_events.PackageSignedDownloaded),
    cqrs.NotificationEvent[domain_events.PackageSignedDownloaded],
)


cqrs.OutboxedEventMap.register(
    get_service_event_name(domain_events.PackageProcessingFailed),
    cqrs.NotificationEvent[domain_events.PackageProcessingFailed],
)
