from flask import Blueprint, request
from flasgger import swag_from

from structure import structure
response_builder = structure.instantiate('response_builder')

auth_blueprint = Blueprint('auth_v1', __name__)

base_swagger_path = './../../documentation/auth'


@auth_blueprint.route('/auth/login', methods=['POST'])
@swag_from(f'{base_swagger_path}/login.yml')
def create_token():
    return structure.instantiate('login_handler').handle(request)


@auth_blueprint.route('/auth/refresh', methods=['POST'])
@swag_from(f'{base_swagger_path}/refresh.yml')
def refresh_token():
    return structure.instantiate('refresh_handler').handle(request)


@auth_blueprint.route('/auth/logout', methods=['POST'])
@swag_from(f'{base_swagger_path}/logout.yml')
def remove_token():
    return structure.instantiate('logout_auth_handler').handle(request)


@auth_blueprint.route('/auth/forgot_password', methods=['POST'])
@swag_from(f'{base_swagger_path}/forgot_password.yml')
def forgot_password():
    return structure.instantiate('forgot_password_handler').handle(request)


@auth_blueprint.route('/auth/reset_password', methods=['POST'])
@swag_from(f'{base_swagger_path}/reset_password.yml')
def reset_password():
    return structure.instantiate('reset_password_handler').handle(request)
