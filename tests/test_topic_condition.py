from pfcm.pfcm import Pfcm, FcmAPI
import os
import yaml
import datetime
import pytest

cur_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(cur_dir)
print(parent_dir)
private_file = os.path.join(parent_dir, 'service_token.json')
with open('config.yml') as f:
    config = yaml.load(f.read())
print(config)
project_name = config["default"]["project_name"]
registration_id = config["default"]["one_token"]


def test_pfcm_send_topic_include_not():
    message_title = "topic"
    message_body = "{} body of message".format(datetime.datetime.now())

    fsmapi = FcmAPI(project_name, private_file)
    pfcm = Pfcm(fsmapi)
    topic = "!('test' in topics) && ('test2' in topics)"
    results = pfcm.send_msg(
        topic_condition=topic,
        message_title=message_title,
        message_body=message_body)

    for result in results:
        print(result)
        assert not "error" in result


@pytest.mark.skip(msg="don't need")
def test_pfcm_send_topic_include_not2():
    message_title = "topic"
    message_body = "{} body of message".format(datetime.datetime.now())

    fsmapi = FcmAPI(project_name, private_file)
    pfcm = Pfcm(fsmapi)
    topic = "!('test' in topics) && ('Global_Topic_Dev' in topics)"
    results = pfcm.send_msg(
        topic_condition=topic,
        message_title=message_title,
        message_body=message_body)

    for result in results:
        print(result)
        assert not "error"  in result


def test_pfcm_send_condition():
    message_title = "topic"
    message_body = "{} body of message".format(datetime.datetime.now())

    fsmapi = FcmAPI(project_name, private_file)
    pfcm = Pfcm(fsmapi)
    topic = "('test' in topics) && ('test2' in topics)"
    results = pfcm.send_msg(
        topic_condition=topic,
        message_title=message_title,
        message_body=message_body)

    for result in results:
        print(result)
        assert not "error"  in result

