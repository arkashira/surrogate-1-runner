import time
from routing.loader import RoutingLoader

def main():
    config_path = '/opt/axentx/surrogate-1/config/routing.yaml'
    routing_loader = RoutingLoader(config_path)

    try:
        routing_loader.load()
        print("Routing table loaded successfully")

        while True:
            if routing_loader.reload_if_changed():
                print("Routing table reloaded due to changes")

            try:
                next_agent = routing_loader.get_next_agent('agent1', 'test_payload')
                print(f"Next agent: {next_agent}")
            except ValueError as e:
                print(f"Routing error: {e}")

            time.sleep(5)
    except Exception as e:
        print(f"Fatal error: {e}")
        raise

if __name__ == '__main__':
    main()