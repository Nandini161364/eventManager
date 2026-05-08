import pytest

from eventsApp.tests.factories import (
    UserFactory,
    EventFactory
)

from eventsApp.adaptors.dtos import CreateBookingDto

from eventsApp.interactors.booking_interactor import BookingInteractor
from eventsApp.storages.booking_storage import BookingStorage
from eventsApp.presenters.booking_presenter import BookingPresenter

from eventsApp.exceptions.exceptions import (
    InvalidDataException,
    EventDoesnotExistException,
    AttendeeDoesnotExist,
    TicketsNotAvailableException,
    AlreadyBookedException
)


@pytest.mark.django_db
class TestCreateBooking:

    def test_create_booking_success(self):

        attendee = UserFactory(role='attendee')

        event = EventFactory()

        bookingDto = CreateBookingDto(
            attendee_id=attendee.id,
            event_id=event.id
        )

        interactor = BookingInteractor(
            storage=BookingStorage(),
            presenter=BookingPresenter()
        )

        response = interactor.create_booking(
            bookingDto
        )

        assert response["message"] == "Booking Created Successfully"
        assert "id" in response