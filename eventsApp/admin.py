from django.contrib import admin
from eventsApp.models import Person, Organizer, Event, Ticket, Feedback, Booking
# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    readonly_fields = ('password',)
    search_fields = ('name', 'email')
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'organization_email')
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'organizer', 'start_date', 'end_date', 'venue', 'is_paid', 'maximum_attendees')

    fieldsets = (
        (None, {
            'fields': ('event_title', 'organizer', 'start_date', 'end_date', 'venue', 'is_paid', 'maximum_attendees')
        }),
        ('Advanced', {
            'fields': ('description',),
        }),
    )
    list_filter = ('organizer', 'start_date', 'end_date', 'is_paid')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    search_fields = ('event_title', 'organizer__organization_name', 'venue')
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('is_paid', 'maximum_attendees', 'start_date', 'end_date', 'venue')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'price')
   

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'comment', 'feedback_date')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'event', 'booking_date', 'booking_status')
    

admin.site.register(Person, PersonAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Booking, BookingAdmin)