from eventsApp.models import Event, Organizer, Ticket

class EventStorage:
    def get_organizer(self, organizer):
        try:
            return Organizer.objects.get(id = organizer)
        except Organizer.DoesNotExist:
            return None
    def create_event(self, eventDto):
        self.eventDto = eventDto
        newEvent = Event.objects.create(event_title = eventDto.event_title, description=eventDto.description, organizer_id=eventDto.organizer, start_date=eventDto.start_date, end_date = eventDto.end_date, is_paid = eventDto.is_paid, maximum_attendees = eventDto.maximum_attendees, venue=eventDto.venue)

        return newEvent.id
    def create_ticket(self, event_id, price):
        self.eventId = event_id
        self.price = price
        newTicket = Ticket.objects.create(event_id = event_id, price=price)

        return newTicket.id