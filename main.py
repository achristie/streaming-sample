import argparse
import ewmd
import asyncio
import json
import logging
import botes_store

logging.basicConfig(
    format="%(asctime)s %(message)s",
    filename="log.log",
    encoding="utf-8",
    level=logging.INFO,
)


def handle_msg(msg):
    j = json.loads(msg)
    if j["action"] == "heartbeat":
        return
    elif j["action"] == "subscribe":
        logging.info(j)


def main():
    db = botes_store.Db()
    with db as db:
        db.create_table()
    client = ewmd.WSClient(**vars(args), callback=handle_msg)
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
