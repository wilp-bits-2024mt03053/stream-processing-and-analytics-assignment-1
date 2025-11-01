.PHONY: up down logs ps clean topic docs

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

clean: down
	rm -rf data/logs/*.log || true
	mkdir -p data/logs && touch data/logs/input.log

topic:
	docker exec -it kafka kafka-topics.sh --bootstrap-server localhost:9092 --create --if-not-exists --topic events --replication-factor 1 --partitions 1 || true

docs:
	@echo "Converting assignment report to PDF..."
	@which pandoc > /dev/null || (echo "Error: pandoc is not installed. Please install pandoc first." && exit 1)
	@which wkhtmltopdf > /dev/null || (echo "Warning: wkhtmltopdf not found. Using basic PDF conversion.")
	@pandoc assignment-report/streaming-assignment-report.md \
		--from markdown \
		--to pdf \
		--output assignment-report/streaming-assignment-report.pdf \
		--pdf-engine=wkhtmltopdf \
		--pdf-engine-opt='--page-size A4' \
		--pdf-engine-opt='--margin-top 20mm' \
		--pdf-engine-opt='--margin-bottom 20mm' \
		--pdf-engine-opt='--margin-left 15mm' \
		--pdf-engine-opt='--margin-right 15mm' \
		--pdf-engine-opt='--encoding UTF-8' \
		--pdf-engine-opt='--print-media-type' \
		--toc \
		--toc-depth=3 \
		--highlight-style=pygments \
		--metadata title="Streaming data analytics for web application" \
		--metadata author="Group 4" \
		--metadata date="$(shell date '+%B %d, %Y')" \
		2>/dev/null || pandoc assignment-report/streaming-assignment-report.md \
		--from markdown \
		--to pdf \
		--output assignment-report/streaming-assignment-report.pdf \
		--pdf-engine=pdflatex \
		--toc \
		--toc-depth=3 \
		--highlight-style=pygments \
		--metadata title="Streaming data analytics for web application" \
		--metadata author="Group 4" \
		--metadata date="$(shell date '+%B %d, %Y')"
	@echo "PDF generated successfully: assignment-report/streaming-assignment-report.pdf"


