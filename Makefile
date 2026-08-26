.PHONY: verify
verify:
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install -q -r apps/api/requirements-dev.txt
	.venv/bin/pytest -q
	@echo career-workspace verify passed
