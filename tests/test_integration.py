import requests
import subprocess
import time

def test_container_runs_and_responds():
    """Integration test for container startup and health check"""
    # Build the Docker image
    subprocess.run(["docker", "build", "-t", "surrogate-1:latest", "."], check=True)

    # Start the container
    container_process = subprocess.Popen(
        ["docker", "run", "-d", "-p", "8080:8080", "surrogate-1:latest"],
        stdout=subprocess.PIPE
    )

    try:
        # Wait for container to start
        time.sleep(5)

        # Verify health endpoint
        response = requests.get("http://localhost:8080/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    finally:
        # Clean up
        container_id = container_process.stdout.read().decode().strip()
        subprocess.run(["docker", "rm", "-f", container_id], check=True)