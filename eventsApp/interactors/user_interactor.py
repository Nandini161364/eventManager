from eventsApp.interactors.presenter_interfaces.user_presenter_interface import UserPresenterInterface
from eventsApp.interactors.storage_interfaces.user_storage_interface import UserStorageInterface

from eventsApp.exceptions.exceptions import InvalidDataException, UserAlreadyExitsException

class CreateUserInteractor:
    def __init__(self, storage: UserStorageInterface, presenter: UserPresenterInterface):
        self.storage = storage
        self.presenter = presenter
    
    def create_user(self, userDto):
        name = userDto.username
        email = userDto.email
        password = userDto.password
        role = userDto.role
        phone_number = userDto.phone_number

        if not (name and email and password and role and phone_number):
            raise InvalidDataException("Data can't be empty")
        if role not in ('organizer', 'attendee'):
            raise InvalidDataException("Role must be organizer or attendee")
        is_existing_mail = self.storage.get_person_by_mail(email)
        if is_existing_mail:
            raise UserAlreadyExitsException("User is already there")
        response = self.storage.create_user(userDto)

        return self.presenter.create_user_success_response(response)
