## Streaming Demo: Flume -> Kafka with Python Producer and Consumer

This demo shows a simple streaming architecture built with Docker:

- Python producer app writes JSON events to a log file
- Apache Flume tails the file and forwards events to Kafka
- Python consumer reads from Kafka and prints simple processing results

### Stack

- Python 3.11
- Apache Flume 1.9
- Apache Kafka 3.6 (with Zookeeper)
- Docker Compose

### Architecture
![image](./images/architecture.png)

### Prerequisites

- Docker and Docker Compose
- For PDF generation: `pandoc` and `wkhtmltopdf` (optional, falls back to `pdflatex`)

### Quickstart

```bash
make clean      # resets data/logs/input.log
make up         # builds and starts containers
make topic      # ensure topic 'events' exists (auto-create is enabled too)
make logs       # follow logs across services
make docs       # convert assignment report to PDF
```

You should see the `producer` writing lines, `flume` forwarding to Kafka, and `consumer` printing messages with a computed price bucket.

### Customization

- Producer rate: set env `PRODUCE_RATE_PER_SEC` in `docker-compose.yml` (default 5)
- Log path: set env `LOG_FILE` (default `/data/logs/input.log`)
- Kafka topic: set env `KAFKA_TOPIC` in consumer and `flume.conf` (default `events`)

### Useful commands

```bash
# List topics
docker exec -it kafka kafka-topics.sh --bootstrap-server localhost:9092 --list

# Read topic directly
docker exec -it kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --from-beginning

# Inspect a single service logs
docker compose logs -f flume
```

### Documentation

- Assignment report: `assignment-report/streaming-assignment-report.md`
- Generate PDF: `make docs` (requires pandoc)
- The PDF will be created at `assignment-report/streaming-assignment-report.pdf`

### Troubleshooting

- If consumer doesn't receive messages, ensure topic exists: `make topic`.
- On Windows/WSL2, file change notifications are reliable via `tail -F`; ensure `/data/logs/input.log` exists (Makefile creates it).
- Flume container uses `exec` source with `tail -F`. For high-throughput or production, prefer `spooldir` source.
- For PDF generation issues, install pandoc: `sudo apt-get install pandoc` (Ubuntu/Debian) or `brew install pandoc` (macOS)


