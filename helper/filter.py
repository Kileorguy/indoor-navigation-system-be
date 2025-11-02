import numpy as np
import math

import logging

logger = logging.getLogger("uvicorn")

def filter_data(data, k=5):
    """Median filter untuk RSSI"""
    return np.median(data)