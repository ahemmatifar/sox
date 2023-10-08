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

.PHONY: lint
lint:
	black .
	ruff --fix .
	mypy --ignore-missing-imports .