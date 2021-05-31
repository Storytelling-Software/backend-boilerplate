import json

from flask import Response


class ResponseBuilder:
    def build(self, response: dict):
        return Response(
            json.dumps(response['body']),
            status=response['status'],
            mimetype='application/json'
        )
