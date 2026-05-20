import logging
from datetime import datetime

class LogFilter:
    def __init__(self, log_level=None, start_time=None, end_time=None):
        self.log_level = log_level
        self.start_time = start_time
        self.end_time = end_time

    def filter_logs(self, logs):
        filtered_logs = []
        for log in logs:
            if self._matches_log_level(log) and self._matches_timestamp(log):
                filtered_logs.append(log)
        return filtered_logs

    def _matches_log_level(self, log):
        if self.log_level is None:
            return True
        return log['level'] == self.log_level

    def _matches_timestamp(self, log):
        if self.start_time is None and self.end_time is None:
            return True
        log_time = datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S')
        if self.start_time and log_time < self.start_time:
            return False
        if self.end_time and log_time > self.end_time:
            return False
        return True


def filter_logs(logs, log_level=None, start_time=None, end_time=None):
    log_filter = LogFilter(log_level, start_time, end_time)
    return log_filter.filter_logs(logs)