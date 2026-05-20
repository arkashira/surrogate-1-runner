from prometheus import PrometheusIntegration

def initialize_prometheus(port=8000):
    """
    Initializes the Prometheus integration.

    :param port: The port on which the Prometheus server will run.
    :return: An instance of PrometheusIntegration.
    """
    return PrometheusIntegration(port)

def send_alert(message):
    """
    Sends an alert message (placeholder for Alertmanager integration).

    :param message: The alert message to send.
    """
    print(f"Alert: {message}")

# Example usage
if __name__ == "__main__":
    prometheus = initialize_prometheus()
    send_alert("Test alert message")