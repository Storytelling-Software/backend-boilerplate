from app import app


class TestApp:
    def setup(self):
        self.client = app.test_client()
        self.context = app.app_context()
        self.context.push()

    def teardown(self):
        self.context.pop()

    def test_apidocs(self):
        response = self.client.get('/apidocs/')

        assert response.status_code == 200

    def test_health_check(self):
        response = self.client.get('/health_check')

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        assert response.data == b'{"message": "Healthy"}'
