import websockets
import requests
import asyncio
import logging


subscription_msg = """
        {
            "action": "subscribe",
            "dataType": "BOTES",
            "criteria": {
              "$and": [
                {
                "key": "Market",
                "operator": "$eq",
                "values": ["EU BFOE"]}
              ]
            }
        }
    """


class WSClient:
    def __init__(self, username, password, apikey, markets, callback):
        self.un = username
        self.pw = password
        self.apikey = apikey
        self.markets = markets
        self.callback = callback

    @staticmethod
    def create_subscription_msg(market):
        return f"""
        {{
            "action": "subscribe",
            "dataType": "BOTES",
            "criteria": {{
              "$and": [
                {{
                "key": "Market",
                "operator": "$eq",
                "values": ["{market}"]}}
              ]
            }}
        }}
    """

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
                for m in self.markets:
                    await ws.send(self.create_subscription_msg(m))
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
