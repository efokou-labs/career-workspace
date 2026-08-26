# career-workspace

Production-style SaaS workload: Next.js UI, FastAPI API + worker, PostgreSQL, Redis, S3-compatible object storage.

It runs on the **shared platform** (kind + GitOps). It does not create its own AWS account.

## Architecture

```text
Browser -> Next.js -> FastAPI -> PostgreSQL
                         |-> worker (Redis)
                         `-> MinIO / S3
```

Environments: Compose (laptop), kind `dev` overlay, documented staging/prod in kubernetes-gitops.

## Verify

```bash
make verify
```

```bash
docker compose up --build
```

API: `http://localhost:8080/healthz`  
Web: `http://localhost:3000`

Secrets never live in Git. Use `.env.example` locally and External Secrets / SOPS on cluster.
