import time
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from models.anomaly_detector import AnomalyDetector

class PodFailureDetector:
    def __init__(self):
        config.load_incluster_config()
        self.v1 = client.CoreV1Api()
        self.anomaly_detector = AnomalyDetector()

    def detect_failures(self):
        while True:
            self.check_pods()
            self.check_daemonsets()
            time.sleep(30)  # Check every 30 seconds

    def check_pods(self):
        try:
            pods = self.v1.list_pod_for_all_namespaces(watch=False)
            for pod in pods.items:
                if pod.status.phase == 'Failed' or self.is_crash_loop_back_off(pod):
                    self.anomaly_detector.report_anomaly(
                        entity_type='pod',
                        entity_name=pod.metadata.name,
                        namespace=pod.metadata.namespace,
                        reason='CrashLoopBackOff' if self.is_crash_loop_back_off(pod) else 'Failed'
                    )
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_pod_for_all_namespaces: {e}")

    def check_daemonsets(self):
        try:
            apps_v1 = client.AppsV1Api()
            daemonsets = apps_v1.list_daemon_set_for_all_namespaces(watch=False)
            for ds in daemonsets.items:
                for pod in ds.status.current_number_scheduled:
                    pod_name = f"{ds.metadata.name}-{pod}"
                    pod = self.v1.read_namespaced_pod(pod_name, ds.metadata.namespace)
                    if pod.status.phase == 'Failed' or self.is_crash_loop_back_off(pod):
                        self.anomaly_detector.report_anomaly(
                            entity_type='daemonset',
                            entity_name=ds.metadata.name,
                            namespace=ds.metadata.namespace,
                            reason='CrashLoopBackOff' if self.is_crash_loop_back_off(pod) else 'Failed'
                        )
        except ApiException as e:
            print(f"Exception when calling AppsV1Api->list_daemon_set_for_all_namespaces: {e}")

    def is_crash_loop_back_off(self, pod):
        for status in pod.status.container_statuses:
            if status.last_state.terminated and status.last_state.terminated.reason == 'Error':
                return True
        return False