import logging

logger = logging.getLogger("uvicorn")

def handle_ws_request(request):
    if request["type"] == "motor":
        logger.info(f"Motor request ${request}")


