import subprocess
import requests
import time

def test_docker_container():
    # Build the Docker image
    build_result = subprocess.run(['docker', 'build', '-t', 'surrogate-1:latest', '.'], check=True)

    # Run the Docker container
    container_id = subprocess.check_output(['docker', 'run', '-d', '-p', '8080:8080', 'surrogate-1:latest']).decode().strip()

    try:
        # Wait for the container to start up
        time.sleep(5)

        # Check the /health endpoint
        response = requests.get('http://localhost:8080/health')
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    finally:
        # Clean up the container
        subprocess.run(['docker', 'rm', '-f', container_id], check=True)