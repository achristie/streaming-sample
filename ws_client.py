import websockets
import get_token
import asyncio


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
    def __init__(
        self,
        username,
        password,
        apikey,
        markets,
        callback=lambda x: print("test"),
    ):
        print(markets)
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

    async def connect(self):
        token = get_token.get_token(self.un, self.pw, self.apikey)
        headers = [("Authorization", f"Bearer {token}")]
        async for ws in websockets.connect(
            "wss://gateway.realtime.platts.com/websocket/v1/subscribe",
            extra_headers=headers,
            ping_interval=None,
        ):
            try:
                for m in self.markets:
                    await ws.send(self.create_subscription_msg(m))
                async for msg in ws:
                    self.callback(msg)
            except websockets.ConnectionClosed as err:
                print("Error: ", err)
                print("Reconnecting in 3 seconds")
                await asyncio.sleep(3)
                token = get_token.get_token(self.un, self.pw, self.apikey)
                headers = [("Authorization", f"Bearer {token}")]
                continue
