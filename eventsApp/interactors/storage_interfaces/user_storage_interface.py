from abc import ABC, abstractmethod
from eventsApp.adaptors.dtos import CreateUserDTO

class UserStorageInterface(ABC):
    @abstractmethod
    def create_user(self, userDto: CreateUserDTO):
        pass
    @abstractmethod
    def get_person_by_mail(self, email: str):
        pass