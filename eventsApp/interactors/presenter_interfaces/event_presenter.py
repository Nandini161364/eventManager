from abc import ABC, abstractmethod

class EventPresenterInterface(ABC):
    @abstractmethod
    def create_event_success_response(self, event_id):
        pass
    @abstractmethod
    def invalid_data(self):
        pass
    @abstractmethod
    def organizer_not_found(self):
        pass