import httpx
import logging

logger = logging.getLogger("uvicorn")

discord_webhook_url = "https://discord.com/api/webhooks/1429084904150536233/a5xRd6SCcY1BYawX3rd5EjPmIA3TtJMsDJ1CTnfLKO2zl1LQvQ9KzLuCwwQWsN3alTaQ"

"""
Function untuk mengirim alert ke discord
"""
async def send_discord_alert(message: str):

    payload = {
        "username": "Nahkoda",
        "embeds": [
            {
                "title": "🚗 Car Navigation Update",
                "description": message,
                "color": 0x00BFFF
            }
        ],
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(discord_webhook_url, json=payload)
            if response.status_code != 204:
                logger.warning(f"Discord webhook returned status {response.status_code}: {response.text}")
    except httpx.RequestError as e:
        logger.error(f"Network error sending Discord alert: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error sending Discord alert: {e}")
