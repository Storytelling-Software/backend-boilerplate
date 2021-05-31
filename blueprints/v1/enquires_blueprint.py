from flask import Blueprint, request
from flasgger import swag_from

from structure import structure

enquires_blueprint = Blueprint('enquires_v1', __name__)

base_swagger_path = './../../documentation/enquires'


@enquires_blueprint.route('/enquiry', methods=['POST'])
@swag_from(f'{base_swagger_path}/send.yml')
def send_enquiry():
    handler = structure.instantiate('send_enquiry_auth_handler')
    return handler.handle(request)
