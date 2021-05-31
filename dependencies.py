import boto3
import mandrill
from wrappers import (
    EnvironmentWrapper,
    PymongoWrapper
)
from celery import Celery
from mailchimp3 import MailChimp


class Dependencies:
    def environment_wrapper(self):
        return EnvironmentWrapper()

    def pymongo_wrapper(self):
        return PymongoWrapper(self.environment_wrapper())

    def mongo(self):
        return self.pymongo_wrapper().get_client()

    def celery(self):
        env = self.environment_wrapper()
        queue_host = env.get_var("RABBITMQ_HOST")
        queue_user = env.get_var("RABBITMQ_USERNAME")
        queue_pass = env.get_var("RABBITMQ_PASSWORD")

        queue_uri = f"amqp://{queue_user}:{queue_pass}@{queue_host}:5672"
        return Celery(
            "onlingo_background",
            broker=queue_uri,
            backend="rpc://",
            include=["background_jobs"],
        )

    def s3_client(self):
        env = self.environment_wrapper()
        aws_access_key_id = env.get_var("AWS_ACCESS_KEY_ID")
        aws_access_secret_key = env.get_var("AWS_SECRET_ACCESS_KEY")
        aws_region = env.get_var("AWS_REGION")
        return boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_access_secret_key,
            region_name=aws_region,
        )

    def s3_resource(self):
        env = self.environment_wrapper()
        session = boto3.Session(
            aws_access_key_id=env.get_var('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=env.get_var('AWS_SECRET_ACCESS_KEY'),
            region_name=env.get_var("AWS_REGION")
        )
        return session.resource('s3')

    def mailchimp(self):
        env = self.environment_wrapper()
        return MailChimp(
            mc_api=env.get_var('MAILCHIMP_API_KEY'), mc_user=env.get_var('MAILCHIMP_USERNAME')
        )

    def mandrill(self):
        env = self.environment_wrapper()
        return mandrill.Mandrill(env.get_var('MANDRILL_API_KEY'))
