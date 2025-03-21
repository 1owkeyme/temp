import abc
import typing
import uuid

import pydantic

from edm.domain import events as domain_events


class Entity(abc.ABC, pydantic.BaseModel):
    model_config = pydantic.ConfigDict(validate_assignment=True)

    guid: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4, frozen=True)


class Aggregate(Entity):
    _events: typing.List[domain_events.DeferredDomainEvent] = pydantic.PrivateAttr(default_factory=list)

    @property
    def events(self) -> typing.List[domain_events.DeferredDomainEvent]:
        return self._events

    def _register_event(self, event: domain_events.DeferredDomainEvent) -> None:
        self._events.append(event)
