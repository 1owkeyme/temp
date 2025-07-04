import typing
from collections import deque

import cqrs
import orjson
from cqrs import NotificationEvent
from cqrs.outbox.repository import EventStatus, OutboxedEvent
from loguru import logger

_TEvents: typing.TypeAlias = deque[dict]


class MockInMemoryOutboxedEventRepository(cqrs.OutboxedEventRepository[None]):
    _common_events: _TEvents = deque()

    def __init__(self, events: _TEvents | None = None) -> None:
        self.__events = events

    def add(self, event: NotificationEvent) -> None:
        registered_event = cqrs.OutboxedEventMap.get(event.event_name)
        if registered_event is None:
            raise TypeError(f"Unknown event name for {event.event_name}")

        if type(event) is not registered_event:
            raise TypeError(
                f"Event type {type(event)} does not match registered event type {registered_event}",
            )

        bytes_payload = orjson.dumps(event.model_dump(mode="json"))

        self._events.append(
            {
                "id": len(self._events) + 1,
                "event_id": event.event_id,
                "event_name": event.event_name,
                "event_status": EventStatus.NEW,
                "created_at": event.event_timestamp,
                "payload": bytes_payload,
                "topic": event.topic,
            },
        )

    async def get_many(self, batch_size: int = 100, topic: typing.Text | None = None) -> typing.List[OutboxedEvent]:
        filtered_events = [event for event in self._events if topic is None or event["topic"] == topic][:batch_size]

        result = []
        for event in filtered_events:
            outboxed_event = self._process_events(event)
            if outboxed_event is None:
                logger.warning(f"Unknown event name for {event['event_name']}")
                continue
            result.append(outboxed_event)

        return result

    async def update_status(self, outboxed_event_id: int, new_status: EventStatus) -> None:
        for event in self._events:
            if event["id"] == outboxed_event_id:
                event["event_status"] = new_status
                return

    async def commit(self):
        pass

    async def rollback(self):
        pass

    @property
    def _events(self) -> _TEvents:
        return self.__events or self._common_events

    def _process_events(self, event_dict: dict) -> OutboxedEvent | None:
        event_model = cqrs.OutboxedEventMap.get(event_dict["event_name"])
        if event_model is None:
            return None

        event_dict["payload"] = orjson.loads(event_dict["payload"])

        return OutboxedEvent(
            id=event_dict["id"],
            topic=event_dict["topic"],
            status=event_dict["event_status"],
            event=event_model.model_validate(event_dict["payload"]),
        )
