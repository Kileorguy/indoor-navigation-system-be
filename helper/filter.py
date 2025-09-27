import numpy as np
import math

import logging

logger = logging.getLogger("uvicorn")

def filter_data(data, k=5):
    median_data = []
    pad = (k-1) // 2

    for i in range(len(data) - k + 1):
        window = data[i:i + k]  # take exactly n elements
        median_data.append(np.median(window))



    return np.mean(median_data)