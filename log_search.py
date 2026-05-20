import re

class LogSearch:
    def __init__(self, keyword=None):
        self.keyword = keyword

    def search_logs(self, logs):
        searched_logs = []
        for log in logs:
            if self._matches_keyword(log):
                searched_logs.append(log)
        return searched_logs

    def _matches_keyword(self, log):
        if self.keyword is None:
            return True
        return re.search(self.keyword, log['message'], re.IGNORECASE)


def search_logs(logs, keyword=None):
    log_search = LogSearch(keyword)
    return log_search.search_logs(logs)