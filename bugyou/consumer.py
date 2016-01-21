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

        self.plugin_list = list()
        self.served_topic = set()
        self.start_listener()

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
        self.passing_data = manager.dict({'plugin_list': self.plugin_list,
                                          'served_topic': self.served_topic})
        proc = Process(target=self.listen_for_instruction,
                       args=(self.passing_data, ))
        proc.start()

    @staticmethod
    def listen_for_instruction(data):
        """ This method listens to instruction queue
        """
        queue = Queue('instruction')
        queue.connect()
        while True:
            task = queue.wait()
            if task.data['type'] == 'create':
                plugin_queue = task.data['queue_name']

                if plugin_queue not in data['plugin_list']:
                    data['plugin_list'].append(plugin_queue)
                    data['served_topic'].extend(task.data['topic'])

    def consume(self, msg):
        """ This is called when we receive a message matching the topic.
        """

        self.served_topic = self.passing_data['served_topic']
        self.plugin_list = self.passing_data['plugin_list']
        topic = msg['body']['topic']

        if topic in self.served_topic:
            for plugin in self.plugin_list:
                queue_attr = 'queue-%s' % plugin
                data = {'topic': topic, 'msg': msg}

                if hasattr(self, queue_attr):
                    queue = getattr(self, queue_attr)
                    queue.enqueue(task)
                else:
                    queue = Queue(plugin)
                    queue.connect()
                    setattr(self, queue_attr, queue)
