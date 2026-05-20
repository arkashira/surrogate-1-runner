from prometheus_client import start_http_server, Gauge, Counter

class PrometheusIntegration:
    def __init__(self, port=8000):
        self.port = port
        self.metrics = {}
        start_http_server(self.port)

    def add_metric(self, name, documentation, metric_type='gauge'):
        """
        Adds a new metric to the Prometheus integration.

        :param name: The name of the metric.
        :param documentation: A brief description of the metric.
        :param metric_type: The type of metric ('gauge' or 'counter').
        """
        if metric_type == 'gauge':
            self.metrics[name] = Gauge(name, documentation)
        elif metric_type == 'counter':
            self.metrics[name] = Counter(name, documentation)
        else:
            raise ValueError("Unsupported metric type. Use 'gauge' or 'counter'.")

    def update_metric(self, name, value):
        """
        Updates the value of an existing metric.

        :param name: The name of the metric to update.
        :param value: The new value to set for the metric.
        """
        if name in self.metrics:
            self.metrics[name].set(value)
        else:
            raise KeyError(f"Metric '{name}' not found. Please add it first.")

# Example usage
if __name__ == "__main__":
    prometheus_integration = PrometheusIntegration()
    prometheus_integration.add_metric('dataset_ingest_count', 'Number of datasets ingested', 'counter')
    prometheus_integration.update_metric('dataset_ingest_count', 10)