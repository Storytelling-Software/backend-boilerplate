from flask import Blueprint
from flasgger import swag_from

from structure import structure
response_builder = structure.instantiate('response_builder')

general_blueprint = Blueprint('general', __name__)

base_swagger_path = './../documentation/general'


@general_blueprint.route('/health_check', methods=['GET'])
@swag_from(f'{base_swagger_path}/health_check.yml')
def health_check():
    response = {
        'body': {
            'message': 'Healthy'
        },
        'status': 200
    }
    return response_builder.build(response)
