APP_NAME=sender
APP_DIR=./$(APP_NAME)/
TEST_DIR=./tests/
SCRIPTS_DIR=./
APP_ENV=integration
PYTHONPATH=./


test_output:
	PYTHONPATH="$(PYTHONPATH)" python3 $(SCRIPTS_DIR)output/main.py

test_input:
	PYTHONPATH="$(PYTHONPATH)" python3 $(SCRIPTS_DIR)input/main.py $(arg)

nats_output:
	PYTHONPATH="$(PYTHONPATH)" python3 $(SCRIPTS_DIR)output/nats_output.py

nats_input:
	PYTHONPATH="$(PYTHONPATH)" python3 $(SCRIPTS_DIR)input/nats_input.py

nats-docker: 
	docker-compose up nats nats-exporter prometheus grafana

nats-stop-docker: 
	docker-compose stop nats nats-exporter prometheus grafana


