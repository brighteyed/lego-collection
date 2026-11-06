IMAGE := lego-collection:latest

.PHONY: all docker install rebuild backup clean

## all: install the Docker image (if required), then run the full backup
all: install backup

## docker: make sure Docker Desktop or OrbStack is running (start it if not)
docker:
	@./scripts/ensure-docker.sh

## install: build the Docker image only if it does not exist yet
install: docker
	@if docker image inspect $(IMAGE) >/dev/null 2>&1; then \
		echo "$(IMAGE) already installed — skipping build (run 'make rebuild' to force)."; \
	else \
		echo "Installing $(IMAGE)..."; \
		docker compose build; \
	fi

## rebuild: force a rebuild of the Docker image
rebuild: docker
	docker compose build

## backup: run the full build, updating the database in DATA_DIR
backup: install
	docker compose run --rm backup

## clean: stop containers and remove the local Docker image
clean:
	docker compose down --rmi local --remove-orphans
