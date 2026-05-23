import weakref
import gc

class StateManager:
    def __init__(self):
        self.states = weakref.WeakValueDictionary()

    def get_state(self, key):
        state = self.states.get(key)
        if state is None:
            state = State()
            self.states[key] = state
        return state

class State:
    def __init__(self):
        self.data = []
        self.gc_threshold = 10000

    def add(self, item):
        self.data.append(item)
        if len(self.data) > self.gc_threshold:
            gc.collect()

# /opt/axentx/surrogate-1/src/parser/core.py
from .state_manager import StateManager

class Parser:
    def __init__(self):
        self.state_manager = StateManager()

    def parse(self, input_stream):
        state = self.state_manager.get_state(id(input_stream))
        for line in input_stream:
            state.add(line)
            # Process line here, e.g., parse, validate, etc.
            # Keep memory usage under control by limiting the number of lines in state.data