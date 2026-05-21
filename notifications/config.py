class EmailConfig:
    def __init__(self, from_email, to_email, smtp_server, smtp_port, password):
        self.from_email = from_email
        self.to_email = to_email
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.password = password

class InAppConfig:
    def __init__(self, url):
        self.url = url

class Config:
    def __init__(self, email_config, in_app_config):
        self.email_config = email_config
        self.in_app_config = in_app_config