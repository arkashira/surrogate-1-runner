from datetime import datetime
from src.support.models import SupportRequest, Feedback

class SupportService:
    def __init__(self):
        self.support_requests = []
        self.feedbacks = []

    def create_support_request(self, issue):
        support_request = SupportRequest(issue)
        support_request.id = len(self.support_requests) + 1
        self.support_requests.append(support_request)
        return support_request

    def get_support_request(self, request_id):
        return next((req for req in self.support_requests if req.id == request_id), None)

    def update_support_request(self, request_id, status):
        request = self.get_support_request(request_id)
        if request:
            request.status = status
            request.updated_at = datetime.now().isoformat()
        return request

    def create_feedback(self, feedback_text):
        feedback = Feedback(feedback_text)
        feedback.id = len(self.feedbacks) + 1
        self.feedbacks.append(feedback)
        return feedback