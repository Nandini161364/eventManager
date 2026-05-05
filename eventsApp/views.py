from rest_framework.decorators import api_view
from rest_framework.response import Response


from eventsApp.adaptors.dtos import CreateEventDTO

from eventsApp.storages.event_storage import EventStorage
from eventsApp.presenters.event_presenter import EventPresenter

from eventsApp.interactors.create_event_interactor import CreateEventInteractor

from eventsApp.exceptions.exceptions import OrganizerNotFoundException, InvalidDataException

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

        eventDto = CreateEventDTO(
            event_title,description,organizer,start_date,end_date,venue,is_paid,maximum_attendees
        )

        interactor = CreateEventInteractor(storage=EventStorage(), presenter=EventPresenter())
        response = interactor.create_event(eventDto)

        return Response(response, 200)
    
    except OrganizerNotFoundException as e:
        return Response(EventPresenter().organizer_not_found(), status=400)
    except InvalidDataException as e:
        return Response(EventPresenter().invalid_data(), status=400)