from eventsApp.models import User

class UserStorage:
    def create_user(self, userDto):
        self.userDto = userDto
        username = userDto.username
        email = userDto.email
        password = userDto.password
        phone_number = userDto.phone_number
        role = userDto.role

        response = User.objects.create_user(username=username, email=email, password=password, role=role, phone_number=phone_number)
        return response.id
    
    def get_person_by_mail(self, email):
        self.email = email

        return User.objects.filter(email=email).exists()
