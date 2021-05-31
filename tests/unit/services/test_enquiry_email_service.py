from mock import Mock

from models import Enquiry
from services import EnquiryEmailService


class TestEnquiryEmailService:
    def setup(self):
        self.celery_mock = Mock()
        self.from_address = 'no-reply@test.com'
        self.to_address = 'test@test.com'
        self.service = EnquiryEmailService(
            self.celery_mock,
            self.from_address,
            self.to_address
        )

        assert self.service.celery == self.celery_mock
        assert self.service.from_address == self.from_address
        assert self.service.to_address == self.to_address

    def test_send_enquiry(self):
        enquiry = Enquiry()
        enquiry.email = 'some partner email'
        enquiry.name = 'some name'
        enquiry.text = 'some text'

        global_merge_vars = [
            {'content': 'some name', 'name': 'FR_NAME'},
            {'content': 'some partner email', 'name': 'FR_EMAIL'},
            {'content': 'some text', 'name': 'FR_MESSAGE'}
        ]
        subject = "Boilerplate Enquiry"

        message = {
            "global_merge_vars": global_merge_vars,
            "subject": subject,
            "to": [
                {
                    "email": self.to_address,
                    "type": "to",
                }
            ],
            "from_email": self.from_address
        }

        self.service.send_enquiry(enquiry)

        self.celery_mock.send_task.assert_called_once_with(
            "background_jobs.send_email",
            [
                'Partner Inquiry', message
            ],
            countdown=0
        )
