"""JSON serialization utilities."""

import numpy as np


def make_json_serializable(obj):
    """Convert numpy arrays to JSON-compatible types."""

    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    # elif isinstance(obj, u.Quantity):
    #     return {'value': obj.value, 'unit': obj.unit}
    elif isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_json_serializable(item) for item in obj]
    return obj
