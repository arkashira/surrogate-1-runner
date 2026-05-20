import subprocess
import time
import sys

HEALTH_CHECK_TIMEOUT = 30

def parse_health_check_logs(container_name):
    """Parse the logs of the PostgreSQL container for health check failures."""
    try:
        # Start a subprocess to tail the logs
        process = subprocess.Popen(
            ["docker", "logs", "-f", container_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        start_time = time.time()
        while time.time() - start_time < HEALTH_CHECK_TIMEOUT:
            output = process.stdout.readline()
            if output:
                if "failed" in output.lower():
                    log_failure(output)
                    process.terminate()
                    return False
            time.sleep(1)
        
        process.terminate()
        return True
    except Exception as e:
        print(f"Error while parsing logs: {e}")
        return False

def log_failure(log_message):
    """Log the failure reason and exit with a non-zero status."""
    print(f"Health check failed: {log_message.strip()}")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python health_check_parser.py <container_name>")
        sys.exit(1)

    container_name = sys.argv[1]
    if not parse_health_check_logs(container_name):
        print("Exiting due to health check failure.")
        sys.exit(1)  # Added sys.exit(1) for consistency