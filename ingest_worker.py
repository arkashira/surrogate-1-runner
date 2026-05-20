import time
import logging
from typing import Dict, List
import statistics

class IngestionWorker:
    def __init__(self):
        self.latency_metrics = {
            'start_times': [],
            'end_times': [],
            'dataset_latencies': {}
        }
        self.logger = logging.getLogger(__name__)

    def process_batch(self, batch: List[Dict]) -> None:
        start_time = time.time()
        dataset_names = [item['dataset'] for item in batch]

        for item in batch:
            self._process_item(item)

        end_time = time.time()
        self._record_latency(start_time, end_time, dataset_names)

    def _process_item(self, item: Dict) -> None:
        # Existing item processing logic
        pass

    def _record_latency(self, start_time: float, end_time: float, dataset_names: List[str]) -> None:
        self.latency_metrics['start_times'].append(start_time)
        self.latency_metrics['end_times'].append(end_time)

        for dataset in dataset_names:
            if dataset not in self.latency_metrics['dataset_latencies']:
                self.latency_metrics['dataset_latencies'][dataset] = []
            self.latency_metrics['dataset_latencies'][dataset].append(end_time - start_time)

        self._log_percentile_latency()

    def _log_percentile_latency(self) -> None:
        if len(self.latency_metrics['end_times']) > 1:
            latencies = [
                end - start
                for start, end in zip(self.latency_metrics['start_times'], self.latency_metrics['end_times'])
            ]
            percentile_99 = statistics.quantiles(latencies, n=100)[-1]
            self.logger.info(f"99th percentile latency: {percentile_99:.2f} seconds")

    def get_average_latency_per_dataset(self) -> Dict[str, float]:
        return {
            dataset: sum(latencies) / len(latencies)
            for dataset, latencies in self.latency_metrics['dataset_latencies'].items()
        }