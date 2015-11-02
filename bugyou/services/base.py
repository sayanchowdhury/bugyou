class BaseService(object):
    """
    Base class for the each service.
    """
    def __init__(self, config):

    def create_issue(self):

    def close_issue(self):

    def update_issue_comment(self):

    def get_issue_title(self, issues):
        """ Returns a set of all the issues title
        :args issues:
        """
        return {issue['title'] for issue in issues}

    def get_issues(self):


    def handle_failed_messages(self):
        """
