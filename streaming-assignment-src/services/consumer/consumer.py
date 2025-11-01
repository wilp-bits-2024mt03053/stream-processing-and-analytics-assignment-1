import json
import os
import sys
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable


def main() -> None:
    bootstrap_servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    topic = os.environ.get("KAFKA_TOPIC", "events")
    group_id = os.environ.get("GROUP_ID", "demo-consumer")

    # Retry loop to wait for Kafka to be ready
    max_attempts = int(os.environ.get("KAFKA_CONNECT_MAX_ATTEMPTS", "60"))
    backoff_seconds = float(os.environ.get("KAFKA_CONNECT_BACKOFF_SEC", "2.0"))

    attempt = 0
    while True:
        attempt += 1
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=bootstrap_servers,
                group_id=group_id,
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            )
            break
        except NoBrokersAvailable as exc:
            if attempt >= max_attempts:
                print(f"Failed to connect to Kafka at {bootstrap_servers} after {attempt} attempts: {exc}", file=sys.stderr, flush=True)
                sys.exit(1)
            print(f"Kafka not ready yet at {bootstrap_servers} (attempt {attempt}/{max_attempts}). Retrying in {backoff_seconds}s...", file=sys.stderr, flush=True)
            time.sleep(backoff_seconds)

    print(f"Consumer connected to {bootstrap_servers}, topic '{topic}', group '{group_id}'", flush=True)
    try:
        for message in consumer:
            event = message.value
            # Simple processing: compute basket value category and print
            price = event.get("product", {}).get("price", 0)
            bucket = "high" if price >= 250 else ("medium" if price >= 50 else "low")
            print(f"offset={message.offset} key={message.key} bucket={bucket} event_id={event.get('event_id')} price={price}")
    except KeyboardInterrupt:
        print("Consumer interrupted, exiting...", file=sys.stderr)
    finally:
        consumer.close()


if __name__ == "__main__":
    main()



