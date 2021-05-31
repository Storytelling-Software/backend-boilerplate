import logging
from gunicorn import glogging


class NoMetricsFilter(logging.Filter):
    def filter(self, record):
        return record.getMessage().find('/metrics') == -1


class CustomLogger(glogging.Logger):

    def setup(self, cfg):
        super().setup(cfg)

        # Add filters to Gunicorn logger
        logger = logging.getLogger("gunicorn.access") 
        logger.addFilter(NoMetricsFilter())
