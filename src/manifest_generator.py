
import yaml
import boto3

def generate_eks_manifest():
    eks = boto3.client('eks')
    cluster_name = "my-eks-cluster"
    cluster = eks.describe_cluster(name=cluster_name)

    manifest = {
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
            manifest["spec"][key] = value

    for role_arn in cluster["cluster"]["roleArn"]:
        manifest["spec"]["roleArn"] = role_arn

    with open("eks_manifest.yaml", "w") as f:
        yaml.dump(manifest, f)

# eks_manifest.yaml
<empty file>