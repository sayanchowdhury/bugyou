# -*- coding: utf-8 -*-

import ConfigParser
import os
import requests

import fedmsg.consumers

import logging
log = logging.getLogger("fedmsg")

class BugyouConsumer(fedmsg.consumers.FedmsgConsumer):

    topic = 'org.fedoraproject.dev.__main__.autocloud.image.success'
    config_key = 'bugyou.consumer.enabled'

    def __init__(self, *args, **kwargs):
        super(BugyouConsumer, self).__init__(*args, **kwargs)

        self.load_config()

        self.base_url = self.config.get('general', 'base_url')
        self.repo_name = self.config.get('general', 'repo_name')
        self.lookup_key_tmpl = "{image_name}-{release}"

    def load_config(self):
        name = '/etc/bugyou/bugyou.cfg'
        if not os.path.exists(name):
            raise Exception('Please add a proper cofig file under /etc/bugyou/')

        self.config = ConfigParser.RawConfigParser()
        self.config.read(name)

    def _get_issue_titles(self, issues):
        """ Returns a set of all the issue title
        """
        return {issue['title'] for issue in issues['issues']}

    def _get_issues(self):
        """ Pull all the issues for a repo in Pagure
        """
        api_url_tmpl = "{base_url}/api/0/{repo_name}/issues"
        api_url = api_url_tmpl.format(base_url=self.base_url,
                                      repo_name=self.repo_name)


        response = requests.get(api_url)

        if not bool(response):
            raise IOError("Failed to talk to %r %r" % (api_url, response))

        return response.json()

    def consume(self, msg):
        """ This is called when we receive a message matching the topic. """

        issues = self._get_issues()
        issue_titles = self._get_issue_titles(issues)

        msg_info = msg['body']['msg']
        image_name = msg_info['image_name']
        release = msg_info['release']

        lookup_key = self.lookup_key_tmpl.format(image_name=image_name,
                                                 release=release)

        if lookup_key in issue_titles:
            print 'YaY! There is a match'
