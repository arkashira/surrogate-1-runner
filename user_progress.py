import json

class UserProgress:
    @staticmethod
    def get_user_progress(user_id):
        """从存储中获取用户进度数据"""
        try:
            with open(f'user_data/{user_id}.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {
                'mastered_terms': [],
                'daily_reminder': None,
                'last_review_date': None
            }

    @staticmethod
    def update_user_progress(user_id, progress):
        """更新用户进度数据"""
        with open(f'user_data/{user_id}.json', 'w') as file:
            json.dump(progress, file, indent=4)