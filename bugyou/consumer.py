# -*- coding: utf-8 -*-

# python core imports
import ConfigParser
import os
from multiprocessing import Process, Manager

# third party packages import
import fedmsg.consumers
from retask import Task
from retask import Queue

# logging
import logging
log = logging.getLogger("fedmsg")


class BugyouConsumer(fedmsg.consumers.FedmsgConsumer):

    topic = ['*']
    config_key = 'bugyou.consumer.enabled'

    def __init__(self, *args, **kwargs):
        super(BugyouConsumer, self).__init__(*args, **kwargs)

        self.load_config()

        log.info("Initializing Plugin list and Topic list")
        self.plugin_list = list()
        self.served_topic = set()

        log.info("Start Listenser")
        self.start_listener()

        log.info("BugyouConsumer is up and ready for action")

    def load_config(self):
        name = '/etc/bugyou/bugyou.cfg'
        if not os.path.exists(name):
            raise Exception('Please add a proper cofig file under /etc/bugyou')

        self.config = ConfigParser.RawConfigParser()
        self.config.read(name)

    def start_listener(self):
        """ This method creates a process for listening to "instruction" queue
        """
        manager = Manager()
        self.arbiter = manager.dict({'plugin_list': self.plugin_list,
                                'served_topic': self.served_topic})

        proc = Process(target=self.listen_for_instruction,
                       args=(self.arbiter, ))
        proc.start()

    @staticmethod
    def listen_for_instruction(arbiter):
        """ This method listens to instruction queue
        """
        queue = Queue('instruction')
        queue.connect()
        while True:
            payload = queue.wait()
            print payload
            if payload.data.get('type') == 'create':
                queue_name = payload.data.get('queue_name')
                topic = payload.data.get('topic')

                if not (queue_name and topic):
                    log.debug('Either queue_name or topic is missing')
                    continue

                print queue_name

                if queue_name not in arbiter['plugin_list']:
                    arbiter['plugin_list'].append(queue_name)
                    arbiter['served_topic'].add(payload.data['topic'])
            print arbiter

    def consume(self, msg):
        """ This is called when we receive a message matching the topic.
        """
        self.served_topic = self.arbiter['served_topic']
        self.plugin_list = self.arbiter['plugin_list']
        topic = msg['body']['topic']

        if topic in self.served_topic:
            log.info('Received a message for the topic({topic})'.format(topic))
            for plugin in self.plugin_list:
                queue_attr = 'queue-{plugin}'.format(plugin)
                data = {
                    'topic': topic,
                    'msg': msg
                }

                if hasattr(self, queue_attr):
                    queue = getattr(self, queue_attr)
                    queue.enqueue(task)
                else:
                    queue = Queue(plugin)
                    queue.connect()
                    setattr(self, queue_attr, queue)
