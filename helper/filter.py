import numpy as np
import math

import logging

logger = logging.getLogger("uvicorn")

def filter_data(data, k=5):
    return np.median(data)