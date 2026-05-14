.PHONY: install test run docker-build compose-up compose-down k8s-apply k8s-delete

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

test:
	pytest

run:
	uvicorn app.main:app --reload

docker-build:
	docker build -t multi-agent-orchestrator:day3 .

compose-up:
	docker compose up --build

compose-down:
	docker compose down

k8s-apply:
	kubectl apply -k k8s/

k8s-delete:
	kubectl delete -k k8s/
