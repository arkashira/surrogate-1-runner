class GuideResolution:
    def __init__(self, id, success_count, total_count):
        self.id = id
        self.success_count = success_count
        self.total_count = total_count

    def to_dict(self):
        return {
            'id': self.id,
            'success_count': self.success_count,
            'total_count': self.total_count
        }