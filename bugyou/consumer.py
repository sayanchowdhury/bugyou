# -*- coding: utf-8 -*-

import ConfigParser
import libpagure
import os

import fedmsg.consumers

import logging
log = logging.getLogger("fedmsg")

ISSUE_CONTENT_TEMPLATE = """
The image {image_name} for the release - {release} failed.
The output can be seen here - {output_url}
"""

class BugyouConsumer(fedmsg.consumers.FedmsgConsumer):

    topic = 'org.fedoraproject.dev.__main__.autocloud.image.success'
    config_key = 'bugyou.consumer.enabled'

    def __init__(self, *args, **kwargs):
        super(BugyouConsumer, self).__init__(*args, **kwargs)

        self.load_config()

        self.access_token = self.config.get('general', 'access_token')
        self.repo_name = self.config.get('general', 'repo_name')

        self.project = libpagure.Pagure(pagure_token=self.access_token,
                                        pagure_repository=self.repo_name)

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
        return {issue['title'] for issue in issues}

    def _get_issues(self):
        """ Pull all the issues for a repo in Pagure
        """
        return self.project.list_issues()

    def _create_issue(self, title, image_name, release, job_id):
        output_url = ("https://apps.fedoraproject.org/autocloud/jobs/"
                           "{task_id}/output".format(job_id=job_id))

        content = ISSUE_CONTENT_TEMPLATE.format(image_name=image_name,
                                                release=release,
                                                output_url=output_url)
        try:
            self.project.create_issue(title=title,
                                      content=content,
                                      private=False)
        except:
            pass

    def consume(self, msg):
        """ This is called when we receive a message matching the topic. """

        issues = self._get_issues()
        issue_titles = self._get_issue_titles(issues)

        msg_info = msg['body']['msg']
        image_name = msg_info['image_name']
        release = msg_info['release']
        topic = msg_info['topic']
        job_id = msg_info['job_id']

        lookup_key = self.lookup_key_tmpl.format(image_name=image_name,
                                                 release=release)
        lookup_key_exists = lookup_key in issue_titles

        if 'failed' in topic:
            if lookup_key_exists:
                self._update_issue_comment()
            else:
                self._create_issue(title=lookup_key,
                                   image_name=image_name,
                                   release=release,
                                   job_id=job_id)
