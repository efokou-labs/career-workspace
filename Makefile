.PHONY: verify verify-api verify-web
verify: verify-api verify-web
	@echo career-workspace verify passed

verify-api:
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install -q -r apps/api/requirements-dev.txt
	.venv/bin/pytest -q

verify-web:
	cd apps/web && npm ci && npm run build
