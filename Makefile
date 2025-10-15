.PHONY: help setup test build deploy clean

help:
	@echo "GENESIS-SOVEREIGN - Make Commands"
	@echo ""
	@echo "setup       - Install dependencies and set up environment"
	@echo "test        - Run all tests"
	@echo "build       - Build Docker images"
	@echo "deploy      - Deploy to AWS"
	@echo "clean       - Clean generated files"
	@echo "local       - Run local development environment"

setup:
	pip install -r requirements.txt
	npm install
	cp .env.example .env
	@echo "Setup complete! Edit .env with your credentials"

test:
	pytest tests/ -v --cov=src

build:
	docker-compose build

local:
	docker-compose up

deploy:
	cd infrastructure/aws/terraform && terraform apply
	kubectl apply -f infrastructure/kubernetes/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf outputs/created-projects/*
