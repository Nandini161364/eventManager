# from oauth2_provider.contrib.rest_framework import OAuth2Authentication
# from oauth2_provider.decorators import protected_resource

import sentry_sdk
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes

from rest_framework.decorators import api_view
from rest_framework.response import Response


from eventsApp.adaptors.dtos import CreateEventDTO, CreateUserDTO, CreateBookingDto, CancelBookingDto, FeedbackDto

from eventsApp.storages.event_storage import EventStorage
from eventsApp.storages.user_storage import UserStorage
from eventsApp.storages.booking_storage import BookingStorage
from eventsApp.storages.feedback_storage import FeedbackStorage

from eventsApp.presenters.event_presenter import EventPresenter
from eventsApp.presenters.user_presenter import UserPresenter
from eventsApp.presenters.booking_presenter import BookingPresenter
from eventsApp.presenters.feedback_presenter import FeedbackPresenter

from eventsApp.interactors.create_event_interactor import CreateEventInteractor
from eventsApp.interactors.user_interactor import CreateUserInteractor
from eventsApp.interactors.booking_interactor import BookingInteractor
from eventsApp.interactors.get_event_details_interactor import GetEventDetailsInteractor
from eventsApp.interactors.feedback_interactor import FeedBackInteractor

from eventsApp.exceptions.exceptions import OrganizerNotFoundException, InvalidDataException, UserAlreadyExitsException, EventDoesnotExistException, AttendeeDoesnotExist, TicketsNotAvailableException, AlreadyBookedException, InvalidBookingIdException, EventNotFoundException, InvalidBookingException, UserCannotCreateEventException

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    try:
        event_title = request.data.get("event_title")
        description = request.data.get("description")
        organizer = request.user
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        venue = request.data.get("venue")
        is_paid = request.data.get("is_paid")
        maximum_attendees = request.data.get("maximum_attendees")
        ticket_price = request.data.get("ticket_price")

        eventDto = CreateEventDTO(
            event_title,description,organizer.id,start_date,end_date,venue,is_paid,maximum_attendees, ticket_price = ticket_price
        )

        interactor = CreateEventInteractor(storage=EventStorage(), presenter=EventPresenter())
        response = interactor.create_event(eventDto)


        return Response(response, 200)
    
    except OrganizerNotFoundException as e:
        return Response(EventPresenter().organizer_not_found(), status=400)
    except InvalidDataException as e:
        return Response(EventPresenter().invalid_data(), status=400)
    except UserCannotCreateEventException as e:
        return Response(EventPresenter().no_access(), status=403)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        role = request.data.get("role")
        phone_number = request.data.get("phone_number")

        user = CreateUserDTO(
            username=username,
            password=password,
            email=email,
            role=role,
            phone_number=phone_number
        )
        interactor = CreateUserInteractor(storage=UserStorage(), presenter=UserPresenter())
        response = interactor.create_user(user)

        return Response(response, 200)

    except UserAlreadyExitsException as e:
        return Response(UserPresenter().invalid_mail(str(e)), 400)
    except InvalidDataException as e:
        return Response(UserPresenter().invalid_data(), 400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def event_booking(request):
    try:
        event_id = request.data.get('event_id')
        attendee_id = request.user.id

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
        sentry_sdk.capture_exception(e)
        return Response(BookingPresenter().seats_full(), 400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking(request):
    try:
        booking_id = request.data.get("booking_id")
        event_id = request.data.get("event_id")
        attendee_id = request.user.id
        cancelBookingDto = CancelBookingDto(booking_id, attendee_id, event_id)

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
@permission_classes([IsAuthenticated])
def get_event_details(request, event_id):
    try:
        interactor = GetEventDetailsInteractor(storage=EventStorage(), presenter = EventPresenter())

        response = interactor.get_event_details(event_id)

        return Response(response, 200)
    except EventNotFoundException as e:
        return Response(EventPresenter().invalid_event(), 400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def give_feedback(request):
    try:
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        event_id = request.data.get('event_id')
        attendee_id = request.user.id

        feedbackDto = FeedbackDto(
            rating, comment, event_id, attendee_id
        )

        interactor = FeedBackInteractor(storage=FeedbackStorage(), presenter=FeedbackPresenter())

        response = interactor.create_feedback(feedbackDto)

        return Response(response, 200)
    except InvalidDataException as e:
        return Response(FeedbackPresenter().invalid_data(), 400)
    except EventNotFoundException as e:
        return Response(FeedbackPresenter().invalid_event(), 400)
    except AttendeeDoesnotExist as e:
        return Response(FeedbackPresenter().invalid_user(), 400)
    except InvalidBookingException as e:
        return Response(FeedbackPresenter().invalid_booking(), 400)

# @api_view(['GET'])
# def get_attendee_details(request):
#     pass

        
