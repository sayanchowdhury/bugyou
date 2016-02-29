# -*- coding: utf-8 -*-
# Copyright (C) 2015 Red Hat, Inc.
#
# bugyou_plugins is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# bugyou_plugins is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# bugyou_plugins.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Sayan Chowdhury  <sayanchowdhury@fedoraproject.org>
#          Subhendu Ghosh   <subho.prp@gmail.com>
#

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
                topics = payload.data.get('topic')
                topics = {topic.strip() for topic in topics.split(',')}

                if not (queue_name and topics):
                    log.debug('Either queue_name or topic is missing')
                    continue

                print queue_name

                if queue_name not in arbiter['plugin_list']:
                    # Dont shout at me. A/C to the documentation, "Modifications
                    # to mutable values or items in dict and list proxies will
                    # not be propagated through the manager, because the proxy
                    # has no way of knowing when its values or items are
                    # modified. To modify such an item, you can re-assign the
                    # modified object to the container proxy"

                    tmp_copy = arbiter['plugin_list']
                    tmp_copy.append(queue_name)
                    arbiter['plugin_list'] = tmp_copy

                    tmp_copy = arbiter['served_topic']
                    tmp_copy = tmp_copy | topics
                    arbiter['served_topic'] = tmp_copy

            print arbiter

    def consume(self, msg):
        """ This is called when we receive a message matching the topic.
        """
        self.served_topic = self.arbiter['served_topic']
        self.plugin_list = self.arbiter['plugin_list']
        topic = msg['topic']

        if topic in self.served_topic:
            log.info('Received a message for the topic({topic})'.format(topic=topic))
            for plugin in self.plugin_list:
                queue_attr = 'queue-{plugin}'.format(plugin=plugin)
                data = {
                    'topic': topic,
                    'msg': msg
                }
                task = Task(data)
                if hasattr(self, queue_attr):
                    queue = getattr(self, queue_attr)
                    queue.enqueue(task)
                else:
                    queue = Queue(plugin)
                    queue.connect()
                    setattr(self, queue_attr, queue)
