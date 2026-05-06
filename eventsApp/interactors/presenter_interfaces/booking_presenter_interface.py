from abc import ABC, abstractmethod
class BookingPresenterInterface(ABC):
    @abstractmethod
    def invalid_event(self):
        pass

    @abstractmethod
    def invalid_attendee(self):
        pass

    @abstractmethod
    def invalid_data(self):
        pass

    @abstractmethod
    def booking_success(self, bookingId: int):
        pass
