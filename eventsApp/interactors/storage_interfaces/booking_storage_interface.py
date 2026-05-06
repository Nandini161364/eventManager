from abc import ABC, abstractmethod
from eventsApp.adaptors.dtos import CreateBookingDto

class BookingStorageInterface(ABC):
    @abstractmethod
    def get_attendee_by_id(self, attendee_id:int):
        pass
    @abstractmethod
    def get_event_by_id(self, event_id:int):
        pass

    @abstractmethod
    def create_booking(self, bookingDto:CreateBookingDto):
        pass

    @abstractmethod
    def seats_available(self, event_id:int):
        pass

    @abstractmethod
    def is_already_booked(self, bookingDto:CreateBookingDto):
        pass