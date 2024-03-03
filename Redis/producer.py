import json
import random
import redis
import logging


def generate_account_number():
    return ''.join(str(random.randint(0, 9)) for _ in range(10))


def generate_json_message():
    message = {
        "metadata": {
            "from": generate_account_number(),
            "to": generate_account_number()
        },
        "amount": random.randint(1000, 100000)
    }
    return json.dumps(message)


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    r = redis.Redis(host='localhost', port=6379, db=0)

    for _ in range(10):
        message = generate_json_message()
        r.publish('queue', message)
        logging.info(message)


if __name__ == "__main__":
    main()
