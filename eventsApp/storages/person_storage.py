from eventsApp.models import Person

class PersonStorage:
    def create_person(self, personDto):
        self.personDto = personDto
        name = personDto.name
        email = personDto.email
        password = personDto.password

        response = Person.objects.create(name=name, email=email, password=password)
        return response.id