import random
import json
import fedmsg
import time

with open('fixtures3.json', 'r') as infile:
    raw_messages = json.load(infile)
    for count,raw_message in enumerate(raw_messages):
        number = random.randint(1, 11)
        time.sleep(number)
        fedmsg.publish(msg=raw_message['msg'],
                       topic='autocloud.image.aborted')
        print "%d published .... "%count

