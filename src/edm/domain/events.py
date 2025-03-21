import abc
import uuid

import cqrs


class DeferredDomainEvent(abc.ABC, cqrs.DomainEvent, frozen=True):
    """
    Базовый класс для событий домена, которые исполняются отложенно.

    В таких событиях необходимо сохранять идентификатор аггрегата, чтобы
    однозначно определять аггрегат, к которому относится такое событие.
    """

    package_id: uuid.UUID


class PackageCreated(DeferredDomainEvent, frozen=True):
    pass


class PackageQueued(DeferredDomainEvent, frozen=True):
    pass


class PackageSigned(DeferredDomainEvent, frozen=True):
    pass


class PackageSignedDownloaded(DeferredDomainEvent, frozen=True):
    pass


class PackageProcessingFailed(DeferredDomainEvent, frozen=True):
    pass
