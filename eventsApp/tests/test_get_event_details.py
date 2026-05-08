import pytest

from eventsApp.tests.factories import (
    BookingFactory,
    EventFactory,
    UserFactory
)

from eventsApp.interactors.get_event_details_interactor import GetEventDetailsInteractor
from eventsApp.storages.event_storage import EventStorage
from eventsApp.presenters.event_presenter import EventPresenter

from eventsApp.exceptions.exceptions import EventNotFoundException


@pytest.mark.django_db
class TestGetEventDetails:

    def test_get_event_details_success(self):

        organizer = UserFactory(role='organizer')
        event = EventFactory(
            organizer=organizer,
            event_title="Standup",
            venue="Gachibowli",
            maximum_attendees=100
        )
        booked_booking = BookingFactory(
            event=event,
            booking_status='booked'
        )
        cancelled_booking = BookingFactory(
            event=event,
            booking_status='cancelled'
        )
        pending_booking = BookingFactory(
            event=event,
            booking_status='pending'
        )

        interactor = GetEventDetailsInteractor(
            storage=EventStorage(),
            presenter=EventPresenter()
        )

        response = interactor.get_event_details(event.id)

        assert response["id"] == event.id
        assert response["event_title"] == "Standup"
        assert response["venue"] == "Gachibowli"
        assert response["maximum_attendees"] == 100
        assert response["organizer_details"][0]["organizer_id"] == organizer.id
        assert response["attendee_details"][0]["attendee_id"] == booked_booking.attendee.id
        assert response["booking_cancelled_users"][0]["attendee_id"] == cancelled_booking.attendee.id
        assert response["booking_pending_users"][0]["attendee_id"] == pending_booking.attendee.id
        assert response["ticket_details"][0]["ticket_price"] == event.tickets.first().price

    def test_get_event_details_with_invalid_event(self):

        interactor = GetEventDetailsInteractor(
            storage=EventStorage(),
            presenter=EventPresenter()
        )

        with pytest.raises(EventNotFoundException):
            interactor.get_event_details(1000)
