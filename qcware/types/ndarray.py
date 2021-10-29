import base64
from typing import Any

import lz4
import numpy as np


def dict_to_ndarray(d: dict):
    if d is None:
        return None
    else:
        b = base64.b64decode(d["ndarray"])
        if d["compression"] == "lz4":
            b = lz4.frame.decompress(b)
        return np.frombuffer(
            b,
            dtype=np.dtype(d["dtype"]),
        ).reshape(d["shape"])


class NDArray(np.ndarray):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            title="NDArray",
            oneOf=[
                {
                    "type": "object",
                    "properties": {
                        "ndarray": {"type": "string"},
                        "compression": {"type": "string"},
                        "dtype": {"type": "string"},
                        "shape": {"type": "array", "items": {"type": "number"}},
                    },
                },
                {"type": "array", "items": {"type": "number"}},
                {
                    "type": "array",
                    "items": {"type": "array", "items": {"type": "number"}},
                },
            ],
        )

    @classmethod
    def validate(cls, v: Any):
        if isinstance(v, np.ndarray):
            return v
        elif isinstance(v, dict):
            return cls.from_dict(v)
        elif isinstance(v, list):
            return np.array(v)
        else:
            raise ValueError("invalid type")

    @classmethod
    def from_dict(cls, d):
        return dict_to_ndarray(d)
