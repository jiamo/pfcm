from pfcm.pfcm import Pfcm, FcmAPI
import os
import yaml
import datetime

cur_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(cur_dir)
print(parent_dir)
private_file = os.path.join(parent_dir, 'service_token.json')
with open('config.yml') as f:
    config = yaml.load(f.read())
print(config)
project_name = config["default"]["project_name"]
registration_id = config["default"]["one_token"]


def test_pfcm_send_one_device():
    message_title = "one device"
    message_body = "{} body of message".format(datetime.datetime.now())
    fsmapi = FcmAPI(project_name, private_file)
    pfcm = Pfcm(fsmapi)
    for i in range(10):
        results = pfcm.send_msg(
            registration_id=registration_id,
            message_title=message_title,
            message_body=message_body,
            with_async=True
        )
        for result in results:
            print(result)
