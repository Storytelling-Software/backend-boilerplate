class Enquiry:
    def __init__(self):
        self.name = None
        self.email = None
        self.text = None

    @staticmethod
    def from_request(attributes: dict):
        enquiry = Enquiry()
        enquiry.name = attributes.get('name', 'Boilerplate Name')
        enquiry.email = attributes.get('email')
        enquiry.text = attributes.get('text')
        return enquiry
