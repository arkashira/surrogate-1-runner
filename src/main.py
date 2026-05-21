from gpu_discovery import GPUDiscovery

def main():
    gpu_discovery = GPUDiscovery()
    gpus = gpu_discovery.detect_gpus()
    print(f"Detected GPUs: {gpus}")

    profile = gpu_discovery.generate_load_balancing_profile()
    print(f"Generated Load Balancing Profile: {profile}")

if __name__ == '__main__':
    main()