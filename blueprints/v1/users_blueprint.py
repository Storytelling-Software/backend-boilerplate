from flask import Blueprint, request
from flasgger import swag_from

from structure import structure

users_blueprint = Blueprint('users_v1', __name__)

base_swagger_path = './../../documentation/users'


@users_blueprint.route('/admins', methods=['POST'])
@swag_from(f'{base_swagger_path}/create_admin.yml')
def create_admin_user():
    handler = structure.instantiate('create_admin_auth_handler')
    return handler.handle(request)


@users_blueprint.route('/users/signup', methods=['POST'])
@swag_from(f'{base_swagger_path}/create.yml')
def create_user():
    handler = structure.instantiate('create_user_auth_handler')
    return handler.handle(request)


@users_blueprint.route('/users', methods=['GET'])
@swag_from(f'{base_swagger_path}/get_page.yml')
def get_users_page():
    handler = structure.instantiate('get_users_page_auth_handler')
    return handler.handle(request)


@users_blueprint.route('/users/search', methods=['GET'])
@swag_from(f'{base_swagger_path}/get_users_search.yml')
def search_users():
    handler = structure.instantiate('search_users_auth_handler')
    return handler.handle(request)


@users_blueprint.route('/users/me', methods=['GET'])
@swag_from(f'{base_swagger_path}/get_me.yml')
def get_me():
    handler = structure.instantiate('get_me_auth_handler')
    return handler.handle(request)


@users_blueprint.route('/users/<user_id>', methods=['GET'])
@swag_from(f'{base_swagger_path}/get_by_id.yml')
def get_user(user_id):
    handler = structure.instantiate('get_user_auth_handler')
    return handler.handle(request, user_id)


@users_blueprint.route('/users/<user_id>', methods=['PUT'])
@swag_from(f'{base_swagger_path}/update.yml')
def update_user(user_id):
    handler = structure.instantiate('update_user_auth_handler')
    return handler.handle(request, user_id)


@users_blueprint.route('/users/<user_id>', methods=['DELETE'])
@swag_from(f'{base_swagger_path}/delete.yml')
def delete_user(user_id):
    handler = structure.instantiate('delete_user_auth_handler')
    return handler.handle(request, user_id)


@users_blueprint.route('/users/confirmation', methods=['POST'])
@swag_from(f'{base_swagger_path}/confirm.yml')
def confirm_user():
    handler = structure.instantiate('confirm_user_handler')
    return handler.handle(request)


@users_blueprint.route('/users/confirmation/resend', methods=['POST'])
@swag_from(f'{base_swagger_path}/resend_confirm.yml')
def resend_confirmation():
    handler = structure.instantiate('resend_user_confirmation_handler')
    return handler.handle(request)


@users_blueprint.route('/users/files', methods=['POST'])
@swag_from(f'{base_swagger_path}/upload_file.yml')
def upload_file():
    handler = structure.instantiate('upload_user_file_auth_handler')
    return handler.handle(request)


@users_blueprint.route('/users/<user_id>/change_password', methods=['POST'])
@swag_from(f'{base_swagger_path}/change_password.yml')
def change_password(user_id):
    return structure.instantiate('change_password_auth_handler').handle(request, user_id)
