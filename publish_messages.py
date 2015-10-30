import random
import json
import fedmsg
import time

count = 0
with open('fixtures.json', 'r') as infile:
    raw_messages= json.load(infile)
    for count,raw_message in enumerate(raw_messages):
        number = random.randint(1, 11)
        time.sleep(1)
        if count == 3:
            break
        #raw_message['topic'] = 'org.fedoraproject.dev.__main__.autocloud.image.success'
        fedmsg.publish(msg=raw_message['msg'], topic=raw_message['topic'][raw_message['topic'].find('autocloud'):])
        count += 1
