from eventsApp.models import Event, Person, Ticket, Booking

class BookingStorage:
    def get_event_by_id(self, event_id):
        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return None
    def get_attendee_by_id(self, attendee_id):
        try:
            return Person.objects.get(id=attendee_id)
        except Person.DoesNotExist:
            return None
    
    def seats_available(self, event_id):
        event = self.get_event_by_id(event_id)
        if not event:
            return None
        maximum_seats =  event.maximum_attendees
        current_seats_count = Booking.objects.filter(event_id=event_id, booking_status = "Booked").count()

        if current_seats_count< maximum_seats:
            return True
        else:
            return False
    
    def create_booking(self, bookingDto):
        self.bookingDto = bookingDto
        event_id = bookingDto.event_id
        attendee_id = bookingDto.attendee_id
        ticket = Ticket.objects.get(event_id=event_id)

        response = Booking.objects.create(
            attendee_id = attendee_id,
            event_id = event_id,
            booking_status = "Booked",
            ticket=ticket
        )

        return response.id
    