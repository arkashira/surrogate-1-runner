import subprocess
import sys

def launch_freerouter():
    try:
        # Launch Freerouter with the current PCB
        process = subprocess.Popen(['freerouter', '--pcb', 'current_pcb.kicad_pcb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error launching Freerouter: {stderr.decode('utf-8')}")
            return False

        print("Freerouter launched successfully")
        return True
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return False

if __name__ == "__main__":
    if not launch_freerouter():
        sys.exit(1)