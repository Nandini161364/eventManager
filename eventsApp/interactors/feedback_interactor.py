from eventsApp.interactors.storage_interfaces.feedback_storage_interface import FeedbackStorageInterface
from eventsApp.interactors.presenter_interfaces.feedback_presenter_interface import FeedbackPresenterInterface

from eventsApp.exceptions.exceptions import AttendeeDoesnotExist, EventNotFoundException, InvalidDataException, InvalidBookingException
class FeedBackInteractor:
    def __init__(self, storage:FeedbackStorageInterface, presenter:FeedbackPresenterInterface):
        self.storage = storage
        self.presenter = presenter

    def create_feedback(self, feedbackDto):
        event_id = feedbackDto.event_id
        attendee_id = feedbackDto.attendee_id
        comment = feedbackDto.comment
        rating = feedbackDto.rating

        is_valid_event = self.storage.is_valid_event(event_id)
        is_valid_user = self.storage.is_valid_user(attendee_id)
        is_booking_available = self.storage.get_booking(feedbackDto)
        is_feedback_already_given = self.storage.is_feedback_already_given(feedbackDto)

        if comment is None or rating is None:
            raise InvalidDataException("Data can't be empty")

        if not is_valid_user:
            raise AttendeeDoesnotExist("Attendee details are invalid")
        if not is_valid_event:
            raise EventNotFoundException("Event doesn't exist")
        if not is_booking_available:
            raise InvalidBookingException("Invalid Booking")
        
        if is_feedback_already_given:
            newFeedbackId = self.storage.update_feedback(feedbackDto)
        else:
            newFeedbackId = self.storage.create_feedback(feedbackDto)

        return self.presenter.create_feedback_response(newFeedbackId)