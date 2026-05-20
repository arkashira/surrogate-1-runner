import subprocess
import sys
from deploy import trigger_workflow, verify_deployment

def main():
    """Single-click deployment automation"""
    try:
        print("[DEPLOY] Validating environment...")
        subprocess.check_call([sys.executable, "-m", "pytest", "tests/deploy_tests.py"])
        
        print("[DEPLOY] Initiating zero-delay workflow...")
        result = trigger_workflow()
        print(f"[STATUS] {result}")
        
        print("[DEPLOY] Verifying deployment integrity...")
        verification = verify_deployment()
        print(f"[RESULT] {verification}")
        
    except Exception as e:
        print(f"[ERROR] Deployment failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()