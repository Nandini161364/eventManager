from abc import ABC, abstractmethod

class FeedbackPresenterInterface(ABC):
    @abstractmethod
    def create_feedback_response(self, feedbackId:int):
        pass
    @abstractmethod
    def is_valid_event(self, eventId:int):
        pass

    @abstractmethod
    def is_valid_user(self, attendeeId:int):
        pass

    @abstractmethod
    def invalid_data(self):
        pass