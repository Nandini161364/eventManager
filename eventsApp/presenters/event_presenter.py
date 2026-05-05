class EventPresenter:
    def create_event_success_response(self, eventId):
        return{
            "message": 'Event Created Successfully',
            "id": eventId
        }
    def organizer_not_found(self):
        return {
            "message": "No Organizer with mentioned Id"
        }
    def invalid_data(self):
        return {
            "message": "Please ensure all the required fields are passed with proper values"
        }