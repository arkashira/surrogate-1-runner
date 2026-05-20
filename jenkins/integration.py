import subprocess
import sys
import os
from pathlib import Path

def run_surrogate_runner():
    """
    Executes the Surrogate-1 dataset ingestion workflow from a Jenkins build step.
    This script is designed to be invoked as a Jenkins build action, handling
    environment variables and command-line arguments to configure the worker
    execution.
    """
    # Detect Jenkins environment by checking JENKINS_URL
    jenkins_url = os.getenv('JENKINS_URL')
    if jenkins_url:
        print("Running in Jenkins environment. Initializing worker...")
    
    # Validate command-line arguments
    if len(sys.argv) < 3:
        print("Error: Missing required arguments. Expected <num_workers> <config_path>")
        sys.exit(1)
    
    try:
        num_workers = int(sys.argv[1])
        config_path = sys.argv[2]
    except ValueError as e:
        print(f"Error: Invalid argument types. {e}")
        sys.exit(1)
    
    # Resolve Surrogate-1 runner path (default to bin directory)
    runner_path = Path(os.environ.get(
        'SURROGATE1_RUNNER_PATH',
        '/opt/axentx/surrogate-1/bin/run_workers.sh'
    ))
    
    if not runner_path.exists():
        print(f"Error: Runner script not found at {runner_path}")
        sys.exit(1)
    
    # Construct command with environment variables for dataset configuration
    cmd = [
        str(runner_path),
        str(num_workers),
        str(config_path),
        # Optional: pass additional environment variables if needed
        os.getenv('SURROGATE1_ENV_VARS', '')
    ]
    
    print(f"Executing command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            env={
                **os.environ,
                'SHARD_ID': os.getenv('JENKINS_JOB_NAME', 'default'),
                'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO')
            }
        )
        
        print("Worker execution completed successfully.")
        print("Standard Output:")
        print(result.stdout)
        
        if result.stderr:
            print("Standard Error:")
            print(result.stderr)
        
        return 0
    except subprocess.CalledProcessError as e:
        print("Worker execution failed with error:")
        print(e.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error during execution: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_surrogate_runner())