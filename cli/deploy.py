import argparse
import os
import subprocess

def deploy_workflow(template_name):
    """
    Deploys a workflow using the provided template name.
    """
    # Check if the template exists
    template_path = f"/opt/axentx/surrogate-1/templates/{template_name}.yaml"
    if not os.path.exists(template_path):
        print(f"Template {template_name} not found.")
        return

    # Deploy the workflow using the template
    subprocess.run(["kubectl", "apply", "-f", template_path])

def main():
    parser = argparse.ArgumentParser(description="Deploy a workflow")
    parser.add_argument("template_name", help="Name of the template to deploy")
    args = parser.parse_args()

    deploy_workflow(args.template_name)

if __name__ == "__main__":
    main()