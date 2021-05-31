from mailchimp3.mailchimpclient import MailChimpError


class EmailSendingService:
    def __init__(self, mandrill_client) -> None:
        self.mandrill_client = mandrill_client

    def send(self, template_name, message) -> None:
        self.mandrill_client.messages.send_template(
            template_name=template_name, template_content=[], message=message
        )


class EmailListService:
    def __init__(self, mailchimp_client, list_id) -> None:
        self.mailchimp_client = mailchimp_client
        self.list_id = list_id

    def add_user(self, user) -> None:
        try:
            mc_data = {
                "email_address": user.email,
                "status": "subscribed",
                'merge_fields': {
                    'FNAME': user.profile.first_name,
                    'LNAME': user.profile.last_name,
                },
            }
            self.mailchimp_client.lists.members.create(self.list_id, mc_data)
        except MailChimpError as e:
            error_message = f"Error adding {user.email} to the mailing list"
            print(error_message, flush=True)


class BaseEmailService:
    def __init__(self, celery, from_address) -> None:
        self.celery = celery
        self.from_address = from_address

    def _compose_message(
        self, user, subject, merge_vars, from_address=None
    ) -> dict:
        if not from_address:
            from_address = self.from_address
        message = {
            "global_merge_vars": self._convert_merge_vars(merge_vars),
            "subject": subject,
            "to": [
                {
                    "email": user.email,
                    "type": "to",
                }
            ],
            "from_email": from_address,
        }
        return message

    def _convert_merge_vars(self, attributes) -> list:
        result = []
        for k, v in attributes.items():
            result.append({"content": v, "name": k})
        return result

    def _schedule_sending(self, template_name, message, delay_seconds=0) -> None:
        self.celery.send_task(
            "background_jobs.send_email",
            [template_name, message],
            countdown=delay_seconds,
        )


class UserEmailService(BaseEmailService):
    def __init__(self, celery, from_address) -> None:
        super().__init__(celery, from_address)

    def recover_password(self, user, code) -> None:
        subject = 'Boilerplate Password Recovery Verification Code'
        merge_vars = {
            'FNAME': user.profile.first_name,
            'FR_RECOVERY_CODE': code
        }
        message = self._compose_message(user, subject, merge_vars)
        self._schedule_sending('Password Recovery', message)

    def send_account_details(self, user, password) -> None:
        subject = 'Your Administrative Account for Boilerplate'
        merge_vars = {
            'FNAME': user.profile.first_name,
            'FR_ACCOUNT_NAME': user.email,
            'FR_ACCOUNT_PASSWORD': password
        }
        message = self._compose_message(user, subject, merge_vars)
        self._schedule_sending('Admin Welcome', message)

    def send_account_confirmation(self, user, code) -> None:
        subject = "Boilerplate Verification Code"
        merge_vars = {
            'FNAME': user.profile.first_name,
            'FR_VERIFICATION_CODE': code
        }
        message = self._compose_message(user, subject, merge_vars)
        self._schedule_sending('SignUp Verification', message)


class EnquiryEmailService(BaseEmailService):
    def __init__(self, celery, from_address, to_address) -> None:
        super().__init__(celery, from_address)
        self.to_address = to_address

    def send_enquiry(self, enquiry, principal=None) -> None:
        subject = 'Boilerplate Enquiry'
        merge_vars = {
            'FR_NAME': enquiry.name,
            'FR_EMAIL': enquiry.email,
            'FR_MESSAGE': enquiry.text
        }
        message = self._compose_message(subject, merge_vars)
        self._schedule_sending('Partner Inquiry', message)

    def _compose_message(self, subject, merge_vars, from_address=None, to_address=None) -> dict:
        if not to_address:
            to_address = self.to_address
        message = {
            "global_merge_vars": self._convert_merge_vars(merge_vars),
            "subject": subject,
            "to": [
                {
                    "email": to_address,
                    "type": "to",
                }
            ],
            "from_email": self.from_address,
        }
        return message
