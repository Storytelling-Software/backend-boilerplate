from background_app import app
from structure import structure
from datetime import datetime


@app.task(bind=True, default_retry_delay=10)
def send_email(self, template_name, message):
    email_sending_service = structure.instantiate('email_sending_service')
    email_sending_service.send(template_name, message)


@app.task(bind=True, default_retry_delay=10)
def update_last_visit(self, user_id, timestamp):
    users_repository = structure.instantiate('users_repository')
    users_repository.update_last_visit(user_id, datetime.fromtimestamp(timestamp))
