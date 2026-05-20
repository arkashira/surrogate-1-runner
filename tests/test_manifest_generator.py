
import unittest
import yaml
import boto3

class TestManifestGenerator(unittest.TestCase):
    def test_eks_manifest(self):
        eks = boto3.client('eks')
        cluster_name = "my-eks-cluster"
        cluster = eks.describe_cluster(name=cluster_name)

        generator = ManifestGenerator()
        manifest = generator.generate_eks_manifest()

        expected_manifest = {
            "apiVersion": "eks.amazonaws.com/v1alpha1",
            "kind": "EksCluster",
            "metadata": {
                "name": cluster_name
            },
            "spec": cluster["cluster"]["resourcesVpcConfig"]["vpcId"],
            "status": {}
        }

        for key, value in cluster["cluster"]["resourcesVpcConfig"].items():
            if key != "vpcId":
                expected_manifest["spec"][key] = value

        for role_arn in cluster["cluster"]["roleArn"]:
            expected_manifest["spec"]["roleArn"] = role_arn

        with open("eks_manifest.yaml", "r") as f:
            actual_manifest = yaml.safe_load(f)

        self.assertEqual(expected_manifest, actual_manifest)

if __name__ == "__main__":
    unittest.main()