
import random
import json

def generate_synthetic_data(data_format: str):
    if data_format == "json":
        return json.dumps({"key1": "value1", "key2": "value2", "key3": "value3"})
    elif data_format == "csv":
        return [
            ["key1", "value1"],
            ["key2", "value2"],
            ["key3", "value3"],
        ]
    elif data_format == "xml":
        return """
        <data>
            <key1>value1</key1>
            <key2>value2</key2>
            <key3>value3</key3>
        </data>
        """
    else:
        raise ValueError("Unsupported data format")