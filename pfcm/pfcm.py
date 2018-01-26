import os
import inspect
import functools
import requests
from oauth2client.service_account import ServiceAccountCredentials
import json


def autoargs(*include, **kwargs):
    def _autoargs(func):
        attrs, varargs, varkw, defaults = inspect.getargspec(func)

        def sieve(attr):
            if kwargs and attr in kwargs['exclude']:
                return False
            if not include or attr in include:
                return True
            else:
                return False

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # handle default values
            # import pdb;pdb.set_trace()
            if defaults:
                for attr, val in zip(reversed(attrs), reversed(defaults)):
                    if sieve(attr):
                        setattr(self, attr, val)
                        if val:
                            self[attr] = val
            # handle positional arguments
            positional_attrs = attrs[1:]
            for attr, val in zip(positional_attrs, args):
                if sieve(attr):
                    setattr(self, attr, val)
                    if val:
                        self[attr] = val
            # handle varargs
            if varargs:
                remaining_args = args[len(positional_attrs):]
                if sieve(varargs):
                    setattr(self, varargs, remaining_args)

            # handle varkw
            if kwargs:
                for attr, val in kwargs.items():
                    if sieve(attr):
                        setattr(self, attr, val)
                        if val:
                            self[attr] = val
            return func(self, *args, **kwargs)

        return wrapper

    return _autoargs


class Playload(dict):
    @autoargs()
    def __init__(self, message=None, validate_only=None):
        super().__init__()


class Message(dict):

    @autoargs()
    def __init__(self, name=None, data=None, notification=None, android=None,
                 webpush=None, apns=None, token=None, topic=None,
                 condition=None):
        super().__init__()

    @property
    def token(self):
        return self.token

    @token.setter
    def token(self, value):
        if value:
            self["token"] = value

    @property
    def topic(self):
        return self.topic

    @topic.setter
    def topic(self, value):
        if value:
            self["topic"] = value

    @property
    def condition(self):
        return self.condition

    @condition.setter
    def condition(self, value):
        if value:
            self["condition"] = value


class RespMessage(dict):

    @autoargs()
    def __init__(self, name=None):
        super().__init__()


class Notification(dict):

    @autoargs()
    def __init__(self, title=None, body=None):
        super().__init__()
        self.title = title
        self.body = body


class AndroidConfig(dict):
    @autoargs()
    def __init__(self, collapse_key=None, priority=None, ttl=None,
                 restricted_package_name=None, data=None,
                 notification=None):
        # google no requirements for this?
        super().__init__()


class AndroidNotification(dict):
    # build this object should not finish
    @autoargs()
    def __init__(self, title=None, body=None, icon=None, color=None, sound=None,
                 tag=None,
                 click_action=None, body_loc_key=None, body_loc_args=None,
                 title_loc_key=None, title_loc_args=None):
        super().__init__()


class WebpushConfig(dict):

    def __init__(self, headers=None, data=None, notification=None):
        super().__init__()


class WebNotification(dict):
    def __init__(self, title, body, icon):
        super().__init__()


class ApnsConfig(dict):
    def __init__(self, headers, payload):
        # payload as json object
        super().__init__()


fsm_scope = 'https://www.googleapis.com/auth/firebase.messaging'


def _get_access_token(private_key_file):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        private_key_file, fsm_scope)
    access_token_info = credentials.get_access_token()
    return access_token_info.access_token


class FcmAPI(object):
    """
    Base class for the pyfcm API wrapper for FCM
    """

    CONTENT_TYPE = "application/json"
    FCM_END_POINT = "https://fcm.googleapis.com/v1/projects/{}/messages:send"
    # FCM only allows up to 1000 reg ids per bulk message.
    FCM_MAX_RECIPIENTS = 1000
    FCM_LOW_PRIORITY = 'normal'
    FCM_HIGH_PRIORITY = 'high'

    def __init__(self, project_name, private_file):
        self.project = project_name
        self.private_file = private_file

    def request_headers(self):
        return {
            "Content-Type": self.CONTENT_TYPE,
            "Authorization": "Bearer " + _get_access_token(self.private_file)
        }

    def do_request(self, payload, timeout, ):
        response = requests.post(
            self.FCM_END_POINT.format(self.project),
            headers=self.request_headers(),
            data=payload,
            timeout=timeout)

        return response

Priority = ["normal", "high"]


class Pfcm():

    def __init__(self, fsmapi):
        self.fsmapi = fsmapi

    def send_msg(self,
                 registration_id=None,
                 registration_ids=None,
                 topic=None,
                 topic_condition=None,
                 message_body=None,
                 message_title=None,
                 data_message=None,
                 android_collapse_key=None,
                 android_time_to_live=None,
                 android_restricted_package_name=None,
                 android_priority=False,
                 android_data_message=None,
                 android_title=None,
                 android_body=None,
                 android_icon=None,
                 android_color=None,
                 android_sound=None,
                 android_tag=None,
                 android_click_action=None,
                 android_body_loc_key=None,
                 android_body_loc_args=None,
                 android_title_loc_key=None,
                 android_title_loc_args=None,
                 apple_headers=None,  # TODO like android explain all args
                 apple_payload=None,  # TODO like android explain all args
                 timeout=5,
                 ):
        notification = Notification(
            title=message_title, body=message_body
        )

        android_nofication = AndroidNotification(
            title=android_title,
            body=android_body,
            icon=android_icon,
            color=android_color,
            sound=android_sound,
            tag=android_tag,
            click_action=android_click_action,
            body_loc_key=android_body_loc_key,
            body_loc_args=android_body_loc_args,
            title_loc_key=android_title_loc_key,
            title_loc_args=android_title_loc_args,
        )
        android_config = AndroidConfig(
            collapse_key=android_collapse_key,
            priority=android_priority,
            ttl=android_time_to_live,
            restricted_package_name=android_restricted_package_name,
            data=android_data_message,
            notification=android_nofication
        )
        apns_config = ApnsConfig(
            headers=apple_headers,
            payload=apple_payload,
        )
        message = Message(
            data=data_message,
            notification=notification,
            android=android_config,
            # we don't care webpush
            apns=apns_config
        )
        target_count = len(list(filter(
            None, [registration_id, registration_ids, topic, topic_condition])))

        if target_count != 1:
            raise Exception(
                "only suport one id or many ids or topic or topic condition")

        playloads = []
        if registration_id:
            message.token = registration_id
            playload = Playload(
                message=message
            )
            playload_json = json.dumps(playload)
            playloads.append(playload_json)

        if registration_ids:
            for registration_id in registration_ids:
                message.token = registration_id
                playload = Playload(
                    message=message
                )
                playload_json = json.dumps(playload)
                playloads.append(playload_json)

        if topic:
            message.topic = topic
            playload = Playload(
                message=message
            )
            playload_json = json.dumps(playload)
            playloads.append(playload_json)

        if topic_condition:
            message.condition = topic_condition
            playload = Playload(
                message=message
            )
            playload_json = json.dumps(playload)
            playloads.append(playload_json)

        result_msgs = []
        for playload_json in playloads:
            result = self.fsmapi.do_request(playload_json, timeout)
            result_msg = self.parse_result(result)
            result_msgs.append(result_msg)

        return result_msgs

    def parse_result(self, response_content):
        return response_content
