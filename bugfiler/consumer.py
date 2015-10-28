# -*- coding: utf-8 -*-

import fedmsg.consumers
import koji

import bugfiler

import logging
log = logging.getLogger("fedmsg")

DEBUG = True


class BugFilerConsumer(fedmsg.consumers.FedmsgConsumer):

    # if DEBUG:
    #     topic = ['org.fedoraproject.dev.__main__.autocloud.image.aborted',
    #              'org.fedoraproject.dev.__main__.autocloud.image.failed',]
    # else:
    #     topic = ['org.fedoraproject.prod.autocloud.image.aborted',
    #              'org.fedoraproject.dev.autocloud.image.failed',]
    if DEBUG:
        topic =  ['org.fedoraproject.dev.autocloud.image.aborted',
                'org.fedoraproject.dev.autocloud.image.failed']
    else:
        topic = ['org.fedoraproject.prod.autocloud.image.aborted',
                'org.fedoraproject.prod.autocloud.image.failed']


    config_key = 'bugfiler.consumer.enabled'

    def __init__(self, *args, **kwargs):
        super(BugFilerConsumer, self).__init__(*args, **kwargs)

    def _get_tasks(self, builds):
        print "task done"

    def consume(self, msg):
        """ This is called when we receive a message matching the topic. """

        builds = list()  # These will be the Koji build IDs to upload, if any.

        msg_info = msg["body"]["msg"]["info"]
        print 'Received %r %r'%(msg['topic'], msg['body']['msg_id'])

        log.info('Received by bugfiler %r %r' % (msg['topic'], msg['body']['msg_id']))


