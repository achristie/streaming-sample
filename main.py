import argparse
import ws_client
import asyncio
import json


def handle_msg(msg):
    print(json.loads(msg))


def main():
    # client = ws_client.WSClient()
    client = ws_client.WSClient(**vars(args), callback=handle_msg)
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
