PYTHON ?= .venv/bin/python
RUFF ?= .venv/bin/ruff
FLUTTER ?= flutter
CFN_LINT ?= .venv/bin/cfn-lint

.PHONY: setup check lint format contract test infra-check catalog-seed api-local mobile-setup mobile-check

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements-dev.lock

check: lint contract test infra-check

lint:
	$(RUFF) check .
	$(RUFF) format --check .

format:
	$(RUFF) check --fix .
	$(RUFF) format .

contract:
	$(PYTHON) PDLC/M4/validar_openapi_runpass.py

test:
	PYTHONPATH=backend $(PYTHON) -m unittest discover -s backend/tests -v

infra-check:
	$(CFN_LINT) -t infra/identity.template.json infra/data.template.yaml -r sa-east-1

catalog-seed:
	PYTHONPATH=backend $(PYTHON) -m runpass.seed_catalog

api-local:
	PYTHONPATH=backend $(PYTHON) -m runpass.local_api

mobile-setup:
	cd mobile && $(FLUTTER) pub get --enforce-lockfile

mobile-check:
	cd mobile && $(FLUTTER) analyze
	cd mobile && dart format --output=none --set-exit-if-changed lib test
	cd mobile && $(FLUTTER) test
