from typing import List, Tuple


def validate_payload(rssi1: List[float], rssi2: List[float], rssi3: List[float]) -> Tuple[bool, str]:
    """Function validasi payload dari MQTT"""
    # return True, "Valid payload"
    if not isinstance(rssi1, list):
        return False, "rssi1 must be a list"
    if not isinstance(rssi2, list):
        return False, "rssi2 must be a list"
    if not isinstance(rssi3, list):
        return False, "rssi3 must be a list"



    if len(rssi1) != 7:
        return False, "rssi1 must contain exactly 7 values"
    if len(rssi2) != 7:
        return False, "rssi2 must contain exactly 7 values"
    if len(rssi3) != 7:
        return False, "rssi3 must contain exactly 7 values"

    return True, "Valid payload"
