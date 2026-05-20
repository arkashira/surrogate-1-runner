const k8s = require('@kubernetes/client-node');

const kc = new k8s.KubeConfig();
kc.loadFromDefault();

const k8sApi = kc.makeApiClient(k8s.Core_v1Api);

exports.getVersion = async () => {
  const response = await k8sApi.listNamespacedPod('kube-system', 'v1');
  return response.body.items[0].metadata.labels.kubernetes_io_os_version;
};