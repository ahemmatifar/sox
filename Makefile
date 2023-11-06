.PHONY: install
install:
	python -m pip install --upgrade pip
	pip install -e .

.PHONY: dev_install
dev_install:
	python -m pip install --upgrade pip
	pip install -e .[dev]

.PHONY: test
test:
	pytest

.PHONY: format
format:
	black .
	ruff format .
	ruff check --fix .
	mypy --ignore-missing-imports .