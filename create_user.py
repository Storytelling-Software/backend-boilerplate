from structure import structure
from faker import Faker
from random import choice
from models import User
from string import ascii_letters


users_repository = structure.instantiate('users_repository')
password_service = structure.instantiate('password_service')
env = structure.dependencies.environment_wrapper().get_var('ENV')
f = Faker()


def generate_password():
    if env != 'prod':
        return 'Boilerplate_password'
    return ''.join(choice(ascii_letters) for i in range(8))


if env == 'prod':
    emails = [
        'dev@storytelling-software.com'
    ]
else:
    emails = [
        'andrei@storytelling-software.com',
        'n.skubak@storytelling-software.com',
        'sergei@storytelling-software.com',
        'd.tsvetkova@storytelling-software.com',
        'd.yartseva@storytelling-software.com',
        'a.shevchenko@storytelling-software.com',
        'd.gusev@storytelling-software.com',
        'a.zhamoidik@storytelling-software.com',
        'a.zlatokurova@storytelling-software.com',
        'nikolay@storytelling-software.com',
        'dev@storytelling-software.com'
    ]

for email in emails:
    existing = users_repository.find_by_email(email)
    if existing:
        continue
    password = generate_password()
    user = User.from_request({
        'email': email,
        'role': 'admin',
        'password_hash': password_service.create_hash(password),
        'first_name': f.first_name(),
        'last_name': f.last_name()
    })
    print(f'Created - {email}/{password}')
    users_repository.create(user)
