# -*- coding: utf-8 -*-

#python core imports
import ConfigParser
import os
from multiprocessing import Process, Manager

#3rd party packages import
import fedmsg.consumers
from retask import Task
from retask import Queue

# logging
import logging
log = logging.getLogger("fedmsg")

ISSUE_CONTENT_TEMPLATE = """
The image {image_name} for the release - {release} failed.
The output can be seen here - {output_url}
"""


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

    def _get_issue_titles(self, issues):
        """
         Returns a set of all the issue title
        """
        return {issue['title'] for issue in issues}

    def _get_issues(self):
        """
         Pull all the issues for a repo in Pagure
        """
        return self.project.list_issues()

    def _create_issue(self, title, content):

        try:
            self.project.create_issue(title=title,
                                      content=content,
                                      private=False)
        except:
            pass

    def _close_issue(self, issue_id):
        try:
            self.project.change_issue_status(issue_id=issue_id,
                                             new_status="Fixed")
        except:
            pass

    def _update_issue_comment(self, issue_id, content):
        try:
            self.project.comment_issue(issue_id=issue_id, body=content)
        except:
            pass

    def start_listener(self):
        """
         Thi method creates a process for listening to "instruction" queue
        """
        manager = Manager()
        self.passing_data = manager.dict({'plugin_list': self.plugin_list,
                                          'served_topic': self.served_topic})
        proc = Process(target=self.listen_for_instruction,
                       args=(self.passing_data, ))
        proc.start()

    @staticmethod
    def listen_for_instruction(data):
        """
         This method listens to instruction queue
        """
        queue = Queue('instruction')
        queue.connect()
        while True:
            task = queue.wait()
            if task.data['type'] == 'create':
                plugin_queue = task.data['queue_name']

                if plugin_queue not in data['plugin_list']:

                    plugin_list = list(data['plugin_list'])
                    plugin_list.append(plugin_queue)
                    data['plugin_list'] = plugin_list

                    topics = list(data['served_topic'])
                    topics.extend(task.data['topic'])
                    data['served_topic'] = set(topics)

    def consume(self, msg):
        """
         This is called when we receive a message matching the topic. 
        """

        self.served_topic = self.passing_data['served_topic']
        self.plugin_list = self.passing_data['plugin_list']
        topic = msg['body']['topic']

        if topic in self.served_topic:
            for plugin in self.plugin_list:
                queue = Queue(plugin)
                data = {'topic': topic, 'msg': msg['body']['msg']}
                task = Task(data)
                queue.connect()
                queue.enqueue(task)
