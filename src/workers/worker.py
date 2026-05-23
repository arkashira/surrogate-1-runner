from notifications import create_email_service

class Worker:
    def __init__(self, pipeline_name, email_service):
        self.pipeline_name = pipeline_name
        self.email_service = email_service

    def run(self):
        try:
            # worker logic here
            pass
        except Exception as e:
            error_snippet = str(e)
            dashboard_link = f"https://dashboard.com/pipeline/{self.pipeline_name}"
            self.email_service.send_alert(self.pipeline_name, error_snippet, dashboard_link, "user@example.com")