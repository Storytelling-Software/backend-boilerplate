import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from structure import deps


def init_sentry():
    env = deps.environment_wrapper()
    sentry_dsn = env.get_var("SENTRY_DSN")
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0
        )
