from ..base_handler import BaseHandler
from models import Enquiry


class SendEnquiryHandler(BaseHandler):
    def __init__(self, enquiry_email_service, response_builder):
        super().__init__(response_builder, None)
        self.enquiry_email_service = enquiry_email_service

    def handle(self, request, principal=None):
        attributes = request.json
        enquire = Enquiry.from_request(attributes)
        return self.execute(principal, self.enquiry_email_service.send_enquiry, enquire)
