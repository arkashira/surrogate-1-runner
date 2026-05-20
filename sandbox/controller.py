import subprocess
import time

def start_kind_cluster():
    subprocess.run(["/opt/axentx/surrogate-1/sandbox/kind_setup.sh"], check=True)

def main():
    start_kind_cluster()
    print("Kubernetes cluster started. Testing can begin.")
    print("Cluster will automatically clean up in 10 minutes.")

if __name__ == "__main__":
    main()