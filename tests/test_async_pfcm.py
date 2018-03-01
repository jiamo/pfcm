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


@pytest.mark.asyncio
async def test_pfcm_send_one_device(event_loop):
    message_title = "one device"
    message_body = "{} body of message".format(datetime.datetime.now())
    fsmapi = FcmAPI(project_name, private_file, event_loop)
    pfcm = Pfcm(fsmapi)
    for i in range(10):
        results = await pfcm.send_msg_async(
            registration_id=registration_id,
            message_title=message_title,
            message_body=message_body)
        for result in results:
            print(result)
