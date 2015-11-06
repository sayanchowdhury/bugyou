class PagureService(object):

    def issues(self):
        """ Returns all the issues for a repo
        """
        return self.project.list_issues()

    def get_issues_titles(self, issues):
        """ Returns a set of all the issue titles
        """
        return {issue['title'] for issue in issues}

    def create_issue(self, title, content):
        try:
            self.project.create_issue(title=title,
                                    content=content,
                                    private=False)
        except:
            pass

    def close_issue(self, issue_id):
        try:
            self.project.comment_issue(issue_id=issue_id,
                                       body=content)
        except:
            pass
