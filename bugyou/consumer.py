# -*- coding: utf-8 -*-

import fedmsg.consumers
import koji

import logging
log = logging.getLogger("fedmsg")

DEBUG = True


class BugyouConsumer(fedmsg.consumers.FedmsgConsumer):

    topic = ['org.fedoraproject.dev.__main__.autocloud.image.success',
             'org.fedoraproject.dev.__main__.autocloud.image.failed']

    config_key = 'bugyou.consumer.enabled'

    def __init__(self, *args, **kwargs):
        super(BugyouConsumer, self).__init__(*args, **kwargs)

    def consume(self, msg):
        """ This is called when we receive a message matching the topic. """

        #from ipdb import set_trace;set_trace()

        builds = list()  # These will be the Koji build IDs to upload, if any.

        msg_info = msg["body"]["msg"]
        print 'Received %r %r'%(msg['topic'], msg['body']['msg_id'])

        log.info('Received by bugfiler %r %r' % (msg['topic'], msg['body']['msg_id']))


