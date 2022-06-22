# pip install asyncio, websockets, aiohttp
import asyncio
import websockets
import aiohttp
import socket
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def get_token():
    url = "https://api.platts.com/auth/api"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "appkey": "ADD_API_KEY",
    }
    body = {
        "username": "ADD_USERNAME",
        "password": "ADD_PASSWORD",
    }
    async with aiohttp.ClientSession() as client:
        async with client.post(url, headers=headers, data=body) as response:
            json_response = await response.json()

            try:
                logger.info(f'access token: {json_response["access_token"]}')
                return json_response["access_token"]
            except:
                logger.error(json_response)
                raise


async def connect():
    url = "wss://gateway.realtime.platts.com/websocket/v1/subscribe"
    subscription_msg = """
        {
            "action": "subscribe",
            "dataType": "WRD-Outages"
        }
    """

    while True:
        # automatically try reconnecting if there is an issue
        try:
            logger.info("Fetching a token")
            token = await get_token()
            headers = [("Authorization", f"Bearer {token}")]

            logger.info(f"Connecting to {url}")
            async with websockets.connect(url, extra_headers=headers) as ws:
                await ws.send(subscription_msg)

                while True:
                    # listen indefinitely
                    try:
                        reply = await asyncio.wait_for(ws.recv(), timeout=200)
                        # handle responses..
                        logger.info(reply)
                    except (
                        websockets.exceptions.ConnectionClosed,
                        asyncio.TimeoutError,
                    ):
                        logger.info("Connection closed. reconnecting in 5 seconds")
                        await asyncio.sleep(5)
                        break
        except socket.gaierror:
            logger.info("Connection issue. reconnecting in 5 seconds")
            await asyncio.sleep(5)
            continue
        except (ConnectionRefusedError, ConnectionAbortedError):
            logger.info("Unable to connect. Retrying in 1 minute")
            await asyncio.sleep(60)
            continue


def main():
    asyncio.run(connect())


if __name__ == "__main__":
    main()
