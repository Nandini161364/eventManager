from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateEventDTO:
    event_title: str
    description: str
    organizer: int
    start_date: datetime
    end_date: datetime
    venue: str
    is_paid: bool
    maximum_attendees: int
    ticket_price: float

@dataclass
class CreatePersonDTO:
    name: str
    email: str
    password: str