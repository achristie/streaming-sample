import websockets
import requests
import asyncio
import logging


class WSClient:
    def __init__(self, username, password, apikey, subscription_msgs, callback):
        self.un = username
        self.pw = password
        self.apikey = apikey
        self.subscription_msgs = subscription_msgs
        self.callback = callback

    @staticmethod
    def get_token(username, password, apikey):
        """Get an Access Token to make API calls with."""
        body = {"username": username, "password": password}
        headers = {"appkey": apikey}
        try:
            r = requests.post(
                "https://api.platts.com/auth/api", data=body, headers=headers
            )
            r.raise_for_status()
            return r.json()["access_token"]
        except Exception as err:
            if r.status_code >= 500:
                logging.error(f"[{r.status_code}] - {err}")
            else:
                logging.error(f"[{r.status_code}] -  {r.json()}")
            raise

    async def connect(self):
        try:
            token = self.get_token(self.un, self.pw, self.apikey)
            headers = [("Authorization", f"Bearer {token}")]
        except Exception as err:
            print("Unable to get token. Check your credentials: ", err)
            return
        async for ws in websockets.connect(
            "wss://gateway.realtime.platts.com/websocket/v1/subscribe",
            extra_headers=headers,
            ping_interval=None,
        ):
            try:
                print("Connected. Check log file for details.")
                for m in self.subscription_msgs:
                    await ws.send(m)
                async for msg in ws:
                    self.callback(msg)
            except websockets.ConnectionClosed as err:
                logging.info("Disconnected! Reconnecting in 3 seconds", err)
                await asyncio.sleep(3)

                try:
                    token = self.get_token(self.un, self.pw, self.apikey)
                    headers = [("Authorization", f"Bearer {token}")]
                except Exception as err:
                    print("Unable to get token. Check your credentials: ", err)
                    return
                continue
