from rest_framework.decorators import api_view
from rest_framework.response import Response


from eventsApp.adaptors.dtos import CreateEventDTO, CreatePersonDTO, CreateBookingDto, CancelBookingDto, FeedbackDto

from eventsApp.storages.event_storage import EventStorage
from eventsApp.storages.person_storage import PersonStorage
from eventsApp.storages.booking_storage import BookingStorage
from eventsApp.storages.feedback_storage import FeedbackStorage

from eventsApp.presenters.event_presenter import EventPresenter
from eventsApp.presenters.person_presenter import PersonPresenter
from eventsApp.presenters.booking_presenter import BookingPresenter
from eventsApp.presenters.feedback_presenter import FeedbackPresenter

from eventsApp.interactors.create_event_interactor import CreateEventInteractor
from eventsApp.interactors.person_interactor import CreatePersonInteractor
from eventsApp.interactors.booking_interactor import BookingInteractor
from eventsApp.interactors.get_event_details_interactor import GetEventDetailsInteractor
from eventsApp.interactors.feedback_interactor import FeedBackInteractor

from eventsApp.exceptions.exceptions import OrganizerNotFoundException, InvalidDataException, UserAlreadyExitsException, EventDoesnotExistException, AttendeeDoesnotExist, TicketsNotAvailableException, AlreadyBookedException, InvalidBookingIdException, EventNotFoundException, InvalidBookingException

@api_view(['POST'])
def create_event(request):
    try:
        event_title = request.data.get("event_title")
        description = request.data.get("description")
        organizer = request.data.get("organizer")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        venue = request.data.get("venue")
        is_paid = request.data.get("is_paid")
        maximum_attendees = request.data.get("maximum_attendees")
        ticket_price = request.data.get("ticket_price")

        eventDto = CreateEventDTO(
            event_title,description,organizer,start_date,end_date,venue,is_paid,maximum_attendees, ticket_price = ticket_price
        )

        interactor = CreateEventInteractor(storage=EventStorage(), presenter=EventPresenter())
        response = interactor.create_event(eventDto)


        return Response(response, 200)
    
    except OrganizerNotFoundException as e:
        return Response(EventPresenter().organizer_not_found(), status=400)
    except InvalidDataException as e:
        return Response(EventPresenter().invalid_data(), status=400)

@api_view(['POST'])
def user_login(request):
    try:
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        #assuming every user as new user for now - later will implement the logic for fetching existing user and creating new only when he is not available in DB

        personDto = CreatePersonDTO(
            name,
            email,
            password
        )

        interactor = CreatePersonInteractor(storage=PersonStorage(), presenter=PersonPresenter())
        response = interactor.create_person(personDto)

        return Response(response, 200)
    except UserAlreadyExitsException as e:
        return Response(PersonPresenter().invalid_mail(), 400)
    except InvalidDataException as e:
        return Response(PersonPresenter().invalid_data(), 400)

@api_view(['POST'])
def event_booking(request):
    try:
        event_id = request.data.get('event_id')
        attendee_id = request.data.get('attendee_id')

        bookingDto = CreateBookingDto(
            event_id,
            attendee_id
        )
        interactor = BookingInteractor(storage=BookingStorage(), presenter=BookingPresenter())

        response = interactor.create_booking(bookingDto)

        return Response(response, 200)

    except InvalidDataException as e:
        return Response(BookingPresenter().invalid_data(), 400)
    except AlreadyBookedException as e:
        return Response(BookingPresenter().already_booked(), 400)
    except EventDoesnotExistException as e:
        return Response(BookingPresenter().invalid_event(), 400)
    except AttendeeDoesnotExist as e:
        return Response(BookingPresenter().invalid_attendee(), 400)
    except TicketsNotAvailableException as e:
        return Response(BookingPresenter().seats_full(), 400)


@api_view(['POST'])
def cancel_booking(request):
    try:
        booking_id = request.data.get("booking_id")
        attendee_id = request.data.get("attendee_id")

        cancelBookingDto = CancelBookingDto(booking_id, attendee_id)

        interactor = BookingInteractor(storage=BookingStorage(), presenter=BookingPresenter())
        response = interactor.cancel_booking(cancelBookingDto)

        return Response(response, 200)
    except AttendeeDoesnotExist as e:
        return Response(BookingPresenter().invalid_attendee(), 400)
    except InvalidDataException as e:
        return Response(BookingPresenter().invalid_data(), 400)
    except InvalidBookingIdException as e:
        return Response(BookingPresenter().invalid_booking(), 400)

@api_view(['GET'])
def get_event_details(request, event_id):
    try:
        interactor = GetEventDetailsInteractor(storage=EventStorage(), presenter = EventPresenter())

        response = interactor.get_event_details(event_id)

        return Response(response, 200)
    except EventNotFoundException as e:
        return Response(EventPresenter().invalid_event(), 400)

@api_view(['POST'])
def give_feedback(request):
    try:
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        event_id = request.data.get('event_id')
        attendee_id = request.data.get('attendee_id')

        feedbackDto = FeedbackDto(
            rating, comment, event_id, attendee_id
        )

        interactor = FeedBackInteractor(storage=FeedbackStorage(), presenter=FeedbackPresenter())

        response = interactor.create_feedback(feedbackDto)

        return Response(response, 200)
    except EventNotFoundException as e:
        return Response(FeedbackPresenter().invalid_event(), 400)
    except AttendeeDoesnotExist as e:
        return Response(FeedbackPresenter().invalid_user(), 400)
    except InvalidBookingException as e:
        return Response(FeedbackPresenter().invalid_booking(), 400)


        
