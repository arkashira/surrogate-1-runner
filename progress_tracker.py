from datetime import datetime
from models.user_progress import UserProgress

class ProgressTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.progress = UserProgress.get_user_progress(user_id)

    def track_term(self, term_id):
        """记录用户掌握的术语"""
        if term_id not in self.progress['mastered_terms']:
            self.progress['mastered_terms'].append(term_id)
            UserProgress.update_user_progress(self.user_id, self.progress)

    def get_mastered_terms(self):
        """获取用户已掌握的术语列表"""
        return self.progress['mastered_terms']

    def set_daily_reminder(self, reminder_time):
        """设置每日提醒时间点"""
        self.progress['daily_reminder'] = reminder_time
        UserProgress.update_user_progress(self.user_id, self.progress)

    def get_daily_reminder(self):
        """获取当前提醒时间点"""
        return self.progress['daily_reminder']

    def set_last_review_date(self):
        """记录上次复习日期"""
        self.progress['last_review_date'] = datetime.now().strftime('%Y-%m-%d')
        UserProgress.update_user_progress(self.user_id, self.progress)

    def should_send_reminder(self):
        """判断是否需要发送提醒（基于上次复习日期）"""
        last_review_date = self.progress.get('last_review_date')
        if not last_review_date:
            return True  # 首次学习无需等待
        days_since_last_review = (datetime.now() - datetime.strptime(last_review_date, '%Y-%m-%d')).days
        return days_since_last_review >= 1  # 每天发送一次提醒