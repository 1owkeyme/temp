import cqrs

from edm.domain import events
from edm.service.handlers import commands as command_handlers
from edm.service.handlers import events as event_handlers
from edm.service.handlers import queries as query_handlers
from edm.service.models import commands, queries


def init_commands(mapper: cqrs.RequestMap) -> None:
    mapper.bind(commands.CreatePackage, command_handlers.CreatePackageHandler)
    mapper.bind(commands.ProcessPackages, command_handlers.ProcessPackagesHandler)
    mapper.bind(commands.ProcessFailedPackages, command_handlers.ProcessFailedPackagesHandler)


def init_queries(mapper: cqrs.RequestMap) -> None:
    mapper.bind(queries.GetDocumentsForCounterparty, query_handlers.GetDocumentsForCounterpartyHandler)


def init_domain_events(mapper: cqrs.EventMap) -> None:
    pass


def init_notification_events(mapper: cqrs.EventMap) -> None:
    mapper.bind(cqrs.NotificationEvent[events.PackageCreated], event_handlers.PackageCreatedHandler)
    mapper.bind(cqrs.NotificationEvent[events.PackageQueued], event_handlers.PackageQueuedHandler)
    mapper.bind(cqrs.NotificationEvent[events.PackageSigned], event_handlers.PackageSignedHandler)
