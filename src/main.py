import threading
from metrics import update_metrics

def main():
    # Start the metrics update thread
    metrics_thread = threading.Thread(target=update_metrics)
    metrics_thread.daemon = True
    metrics_thread.start()

    # Your existing code here
    # ...

if __name__ == "__main__":
    main()