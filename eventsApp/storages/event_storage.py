from eventsApp.models import Event, User, Ticket
from eventsApp.interactors.storage_interfaces.event_storage_interface import EventStorageInterface
from eventsApp.adaptors.dtos import EventDetailsDto, OrganizerDetailsDto, AttendeeDetailsDto, TicketDetailsDto

class EventStorage(EventStorageInterface):
    def get_organizer(self, organizer):
        try:
            return User.objects.get(id = organizer)
        except User.DoesNotExist:
            return None
    def create_event(self, eventDto):
        
        newEvent = Event.objects.create(event_title = eventDto.event_title, description=eventDto.description, organizer_id=eventDto.organizer, start_date=eventDto.start_date, end_date = eventDto.end_date, is_paid = eventDto.is_paid, maximum_attendees = eventDto.maximum_attendees, venue=eventDto.venue)

        return newEvent.id
    def create_ticket(self, event_id, price):
        newTicket = Ticket.objects.create(event_id = event_id, price=price)

        return newTicket.id
    
    def is_valid_event(self, event_id):
        try:
            return Event.objects.filter(id=event_id).exists()
        except Event.DoesNotExist:
            return None
         
    def get_event_details(self, event_id):
        event = Event.objects.select_related('organizer').prefetch_related(
            'tickets',
            'bookings__attendee'
        ).get(id=event_id)

        eventData = EventDetailsDto(
            id = event.id,
            event_title = event.event_title,
            description = event.description,
            start_date = event.start_date,
            end_date = event.end_date,
            venue = event.venue,
            maximum_attendees = event.maximum_attendees,
            organizer_details = [
                OrganizerDetailsDto(
                    organizer_id = event.organizer.id,
                    organizer_email=event.organizer.email,
                    organizer_name=event.organizer.username,
                )
            ],
            attendee_details = [
                AttendeeDetailsDto(
                    attendee_id= booking.attendee.id,
                    attendee_email=booking.attendee.email,
                    attendee_name=booking.attendee.username
                ) for booking in event.bookings.filter(booking_status='booked')
            ],
            booking_cancelled_users = [
                AttendeeDetailsDto(
                    attendee_id= booking.attendee.id,
                    attendee_email=booking.attendee.email,
                    attendee_name=booking.attendee.username
                ) for booking in event.bookings.filter(booking_status='cancelled')
            ],
            booking_pending_users =[
                AttendeeDetailsDto(
                    attendee_id= booking.attendee.id,
                    attendee_email=booking.attendee.email,
                    attendee_name=booking.attendee.username
                ) for booking in event.bookings.filter(booking_status='pending')
            ],
        
            ticket_details= [
                TicketDetailsDto(
                    ticket_price=ticket.price
                ) for ticket in event.tickets.all()
            ]

        )

        return eventData
