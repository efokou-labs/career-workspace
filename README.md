# Askel

Kind GitOps workload for [Askel](https://www.getaskel.com/) — your job search, one step at a time.

Production runs on Vercel + Neon. This repo is the **shared-platform** copy: Next.js UI, FastAPI API + worker, PostgreSQL, Redis, S3-compatible object storage. It does not create its own AWS account.

## Architecture

```text
Browser -> Next.js -> FastAPI -> PostgreSQL
                         |-> worker (Redis)
                         `-> MinIO / S3
```

Environments: Compose (laptop), kind `dev` overlay, documented staging/prod in kubernetes-gitops.

On kind, the `dev` overlay runs Postgres and Redis in-cluster (emptyDir, demo credentials labeled `demo: kind-only`). Port-forward the UI with `kubectl -n askel port-forward svc/askel-web 3000:80`.

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

## License

The source code for this project is licensed under the MIT License. Personal content, including my resume, photographs, written content, branding, and other identifying materials, is not covered by this license and may not be reused without permission.

See [LICENSE](LICENSE).
