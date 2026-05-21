import unittest
from kubernetes import client

class TestDeployment(unittest.TestCase):
    def test_deployment(self):
        v1 = client.CoreV1Api()
        deployment = v1.read_namespaced_deployment(name='surrogate-1', namespace='default')
        self.assertEqual(deployment.spec.replicas, 16)

if __name__ == '__main__':
    unittest.main()