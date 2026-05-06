from eventsApp.exceptions.exceptions import InvalidDataException, EventDoesnotExistException, AttendeeDoesnotExist, TicketsNotAvailableException, AlreadyBookedException
from eventsApp.interactors.presenter_interfaces.booking_presenter_interface import BookingPresenterInterface
from eventsApp.interactors.storage_interfaces.booking_storage_interface import BookingStorageInterface

class BookingInteractor:
    def __init__(self, storage: BookingStorageInterface, presenter:BookingPresenterInterface):
        self.storage = storage
        self.presenter = presenter

    def create_booking(self, bookingDto):
        self.bookingDto = bookingDto

        event_id = bookingDto.event_id
        attendee_id = bookingDto.attendee_id

        does_event_exist = self.storage.get_event_by_id(event_id)
        does_attendee_exist = self.storage.get_attendee_by_id(attendee_id)
        seats_available = self.storage.seats_available(event_id)
        is_already_booked = self.storage.is_already_booked(bookingDto)

        if not (event_id and attendee_id):
            raise InvalidDataException("Data can't be empty")
        if not does_event_exist:
            raise EventDoesnotExistException("Event is not present")
        if not does_attendee_exist:
            raise AttendeeDoesnotExist("Attendee is not there")
        if is_already_booked:
            raise AlreadyBookedException("Already registered")
        if not seats_available:
            raise TicketsNotAvailableException("Tickets not Available")
        
        newBookingId = self.storage.create_booking(bookingDto)

        return self.presenter.booking_success(newBookingId)

        
