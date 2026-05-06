from abc import ABC, abstractmethod


class PersonPresenterInterface(ABC):
    @abstractmethod
    def create_person_success_response(self, personId):
        pass

    @abstractmethod
    def invalid_data(self):
        pass