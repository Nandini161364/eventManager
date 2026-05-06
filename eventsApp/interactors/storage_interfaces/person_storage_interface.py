from abc import ABC, abstractmethod
from eventsApp.adaptors.dtos import CreatePersonDTO

class PersonStorageInterface(ABC):
    @abstractmethod
    def create_person(self, personDto: CreatePersonDTO):
        pass
