import json
import argparse
import redis
import logging


def process_message(message, bad_guys):
    json_message = json.loads(message)
    from_account = json_message["metadata"]["from"]
    to_account = json_message["metadata"]["to"]
    amount = json_message["amount"]

    if to_account in bad_guys and amount > 0:
        json_message["metadata"]["from"], json_message["metadata"]["to"] = to_account, from_account
        logging.info(json.dumps(json_message))
    else:
        logging.info(json.dumps(json_message))


def main():
    parser = argparse.ArgumentParser(description='Consumer for Redis pubsub queue')
    parser.add_argument('-e', '--bad_guys', required=True, type=str, help='List of bad guys account numbers separated by comma')
    args = parser.parse_args()
    bad_guys = args.bad_guys.split(',')

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    r = redis.Redis(host='localhost', port=6379, db=0)

    pubsub = r.pubsub()
    pubsub.subscribe('queue')

    for message in pubsub.listen():
        if message['type'] == 'message':
            process_message(message['data'], bad_guys)


if __name__ == "__main__":
    main()
