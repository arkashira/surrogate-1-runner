import logging

def emit_event(event_name, event_data):
    logging.info(f'Emitting event {event_name} with data {event_data}')
    # Add logic to emit event to downstream consumers