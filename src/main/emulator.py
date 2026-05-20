import argparse
import sys
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

from .config_validator import load_config, validate_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DummyHandler(BaseHTTPRequestHandler):
    """
    Simple HTTP handler that mimics a Datadog API endpoint.
    """

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Datadog emulator response")

    def log_message(self, format, *args):
        # Override to suppress default logging to stderr
        logger.info("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format % args))


def run_server(port: int = 8080):
    """
    Start a basic HTTP server on the specified port.
    """
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    logger.info(f"Starting Datadog emulator on port {port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down emulator")
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description="Datadog emulator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Start command
    start_parser = subparsers.add_parser("start", help="Start the emulator")
    start_parser.add_argument("service", choices=["datadog"], help="Service to emulate")
    start_parser.add_argument("--config", required=True, help="Path to YAML config file")

    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop the emulator")
    stop_parser.add_argument("service", choices=["datadog"], help="Service to stop")

    args = parser.parse_args()

    if args.command == "start" and args.service == "datadog":
        try:
            cfg = load_config(args.config)
            validate_config(cfg)
            logger.info(f"Loaded config: {cfg}")
        except Exception as exc:
            logger.error(f"Configuration error: {exc}")
            sys.exit(1)

        run_server()
    elif args.command == "stop" and args.service == "datadog":
        # Placeholder: In a real implementation, this would signal the running process.
        logger.info("Stop command received – no running process to stop in this stub.")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()