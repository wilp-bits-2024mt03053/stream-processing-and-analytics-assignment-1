import os
import sys
import json
import time
import random
from datetime import datetime, timezone
from faker import Faker


def generate_event(fake: Faker) -> dict:
    return {
        "event_id": fake.uuid4(),
        "ts": datetime.now(timezone.utc).isoformat(),
        "user": {
            "id": fake.random_int(min=1, max=1_000_000),
            "name": fake.name(),
            "email": fake.email(),
        },
        "action": random.choice(["view", "click", "purchase", "add_to_cart", "logout"]),
        "product": {
            "id": fake.random_int(min=1, max=10_000),
            "name": fake.word(),
            "price": round(random.uniform(5.0, 500.0), 2),
            "currency": "USD",
        },
        "metadata": {
            "user_agent": fake.user_agent(),
            "ip": fake.ipv4_public(),
            "ref": fake.uri(),
        },
    }


def main() -> None:
    log_file_path = os.environ.get("LOG_FILE", "/data/logs/input.log")
    rate_per_sec = int(os.environ.get("PRODUCE_RATE_PER_SEC", "5"))
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    fake = Faker()
    print(f"Producer writing to {log_file_path} at ~{rate_per_sec} events/sec", flush=True)

    with open(log_file_path, "a", buffering=1) as f:
        while True:
            start = time.time()
            for _ in range(rate_per_sec):
                event = generate_event(fake)
                f.write(json.dumps(event) + "\n")
            elapsed = time.time() - start
            sleep_for = max(0.0, 1.0 - elapsed)
            time.sleep(sleep_for)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Producer interrupted, exiting...", file=sys.stderr)


