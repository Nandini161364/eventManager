from abc import ABC, abstractmethod
from eventsApp.adaptors.dtos import FeedbackDto

class FeedbackStorageInterface:
    @abstractmethod
    def is_valid_event(self, eventId:int):
        pass
    
    @abstractmethod
    def create_feedback(self, feedbackDto:FeedbackDto):
        pass

    @abstractmethod
    def is_valid_user(self, attendeeId: int):
        pass

    @abstractmethod
    def get_booking(self, feedbackDto: FeedbackDto):
        pass
    
    @abstractmethod
    def is_feedback_already_given(self, feedbackDto: FeedbackDto):
        pass

    @abstractmethod
    def update_feedback(self, feedbackDto: FeedbackDto):
        pass
