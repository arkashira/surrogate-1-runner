import argparse
from telemetry import send_telemetry
from config import get_config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Command to execute')
    parser.add_argument('--disable-telemetry', action='store_true', help='Disable telemetry')
    args = parser.parse_args()

    if args.disable_telemetry:
        config = get_config()
        config.telemetry_enabled = False
        config.save()

    # Execute command
    print(f'Executing command: {args.command}')

    # Send telemetry
    send_telemetry(args.command, '2023-03-01 12:00:00', 'Ubuntu 20.04')

if __name__ == '__main__':
    main()