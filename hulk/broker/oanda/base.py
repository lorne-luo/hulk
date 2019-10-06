import settings
import v20

from .common.constants import OANDA_ENVIRONMENTS
from ...utils.singleton import SingletonDecorator

OANDA_API_DOMAIN = OANDA_ENVIRONMENTS["api"][settings.OANDA_DOMAIN]
OANDA_STREAM_DOMAIN = OANDA_ENVIRONMENTS["streaming"][settings.OANDA_DOMAIN]


def create_api_context():
    """
    Initialize an API context based on the Config instance
    """
    ctx = v20.Context(
        hostname=OANDA_API_DOMAIN,
        application=settings.APPLICATION_NAME,
        token=settings.OANDA_ACCESS_TOKEN,
    )

    return ctx


def create_streaming_context():
    """
    Initialize a streaming API context based on the Config instance
    """
    ctx = v20.Context(
        hostname=OANDA_STREAM_DOMAIN,
        application=settings.APPLICATION_NAME,
        token=settings.OANDA_ACCESS_TOKEN,
        datetime_format='RFC3339'
    )

    return ctx


SingletonAPIContext = SingletonDecorator(v20.Context)

api = SingletonAPIContext(hostname=OANDA_API_DOMAIN,
                          application=settings.APPLICATION_NAME,
                          token=settings.OANDA_ACCESS_TOKEN)

stream_api = SingletonAPIContext(hostname=OANDA_STREAM_DOMAIN,
                                 application=settings.APPLICATION_NAME,
                                 token=settings.OANDA_ACCESS_TOKEN)

