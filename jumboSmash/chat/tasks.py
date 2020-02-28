import logging
import time
from functools import wraps
from celery import shared_task
from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from .models import Message


def retry(exc, tries=4, delay=3, backoff=2):
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exc:
                    logging.error(exc.errors)
                    logging.error(exc.response_data)
                    logging.warning("retrying")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry

    return deco_retry


@shared_task
def message_task(message, recipient):
    Message.objects.update_delivered(message["id"])
    if recipient.push_token:
        send_push_message(recipient, message)
    return "message delivered"


@retry((PushResponseError, ConnectionError, HTTPError))
def send_push_message(recipient, message, extra=None):
    try:
        response = PushClient().publish(
                PushMessage(to=recipient.push_token,
                            body=message,
                            data=extra))
    except PushServerError as exc:
        logging.error(exc.errors)
        logging.error(exc.response_data)
        raise

    try:
        response.validate_response()
    except DeviceNotRegisteredError as exc:
        recipient.update_push_token(None)
        logging.error(exc)