import argparse
import ws
import asyncio
import json
import logging
import ewmd_store

logging.basicConfig(
    format="%(asctime)s %(message)s",
    filename="log.log",
    encoding="utf-8",
    level=logging.INFO,
)


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


def handle_msg(db):
    def f(msg):
        j = json.loads(msg)
        if j["action"] == "data":
            db.insert(j["message"])
        logging.info(j)

    return f


def main():
    db = ewmd_store.Db()
    sm = [create_subscription_msg(m.strip()) for m in args.markets]
    db.create_table()
    client = ws.WSClient(
        args.username, args.password, args.apikey, sm, callback=handle_msg(db)
    )
    asyncio.run(client.connect())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-u", "--username", required=True, help="Username", dest="username"
    )
    parser.add_argument(
        "-p", "--password", required=True, help="Password", dest="password"
    )
    parser.add_argument("-a", "--apikey", required=True, help="ApiKey", dest="apikey")
    parser.add_argument(
        "-m",
        "--markets",
        required=True,
        help="Markets to subscribe to",
        dest="markets",
        type=lambda s: [i for i in s.split(",")],
    )

    args = parser.parse_args()

    main()
