# -*- coding: utf-8 -*-
import fedmsg.consumers

import logging
log = logging.getLogger("fedmsg")

class BugyouConsumer(fedmsg.consumers.FedmsgConsumer):

    topic = 'org.fedoraproject.dev.__main__.autocloud.image.success'
    config_key = 'bugyou.consumer.enabled'

    def __init__(self, *args, **kwargs):
        super(BugyouConsumer, self).__init__(*args, **kwargs)

    def _get_issue_title(self, issues):
        """ Returns a tuple of all the issues name
        """
        print issues

    def _get_issues(self):
        """ Pull all the issues for a repo in Pagure
        """
        api_url_tmpl = "{{ base_url }}/api/0/{{ repo_name }}/issues/"
        api_url = api_url_tmpl.format(base_url=self.base_url,
                                      repo_name=self.repo_name)

        response = requests.get(api_url)

        if not bool(response):
            raise IOError("Failed to talk to %r %r" % (url, response))

        return response.json()

    def consume(self, msg):
        """ This is called when we receive a message matching the topic. """
        self.base_url = self.config_get('base_url')
        self.repo_name = self.config_get('repo_name')

        issues = self._get_issues()
