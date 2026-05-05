from eventsApp.adaptors.dtos import CreateEventDTO
from abc import ABC, abstractmethod


class EventStorageInterface(ABC):
    @abstractmethod
    def create_event(self, event_dto: CreateEventDTO):
        pass
    @abstractmethod
    def get_organizer(self, organizerId: int):
        pass