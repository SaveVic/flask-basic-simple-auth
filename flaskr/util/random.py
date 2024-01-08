from faker import Faker

from flaskr.model.user import UserModel

fake = Faker()


def get_random_user() -> UserModel:
    profile = fake.simple_profile()
    username = profile['username']
    email = profile['mail']
    password = fake.password(length=12)
    return UserModel(username=username, email=email, password=password)
