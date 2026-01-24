# 📘 Learnings

## 1️⃣ What `$PATH` means (and why it matters)

`$PATH` is an environment variable that tells Linux **where to look for executable commands**.

When you run:

`python`

Linux searches directories listed in `$PATH` **from left to right** and runs the first `python` it finds.

Example:

`ENV PATH="/app/.venv/bin:$PATH"`

This ensures:

* `/app/.venv/bin/python` is found **before** system Python

* The virtual environment is effectively “activated” without running `source activate`

* * *

## 2️⃣ What `uv run` actually does

`uv run` is **not magic** and does **not install dependencies**.

What it does:

* Locates the project’s virtual environment (`.venv`)

* Temporarily prepends `.venv/bin` to `$PATH`

* Runs the given command

* Restores `$PATH` afterward

So:

`uv run python script.py`

is effectively:

`(PATH=.venv/bin:$PATH) python script.py`

If `$PATH` already includes `.venv/bin`, `uv run` is **not needed** at runtime.

* * *

## 3️⃣ Where Docker named volumes reside

When using a Docker named volume like:

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

`-v ny_taxi_postgres_data:/var/lib/postgresql/data`

The data:

* **Does NOT live in the project directory**

* Is managed by Docker internally

On Linux, the actual location is:

`/var/lib/docker/volumes/ny_taxi_postgres_data/_data`

You can inspect it using:

`docker volume inspect ny_taxi_postgres_data`

Named volumes persist even if containers are deleted.

## 4 Docker Networking Note: localhost vs Containers

Core Rule

> **localhost always means “this machine.”**

In Docker, _which_ machine depends on where the code is running.

The Three Contexts

### 1\. Host Machine (Your PC)

* localhost → **your PC**

* PC localhost:5432 → Postgres container:5432

* Useful for tools like psql, GUI clients, browsers, etc.

### 2\. Inside a Container (e.g. Ingestion Script)

* localhost → **that container itself**

* It does **NOT** mean:

  * your PC

  * another container

Using host="localhost" here will fail unless the service runs in the **same container**.

### 3\. Inside the Postgres Container

* localhost → **Postgres container**

* PostgreSQL is running here

psql -h localhost works _inside this container_

How Containers Talk to Each Other

* Containers communicate over a **Docker network**

* Use **service/container names** as hostnames

### Example (Docker Compose)

`services:    postgres:      image: postgres    ingestor:      image: my-ingestion-image`

Connection from ingestion container:
`host = "postgres"  port = 5432`

Docker provides built-in DNS → postgres resolves automatically

Critical Rule to Remember

> **Port mappings are ONLY for host ↔ container communication**

* Containers **ignore** -p mappings

* Container ↔ container traffic is **direct over the network**

Mental Model

`Your PC (host)  └── localhost:5432       │  (port mapping)       ▼  Postgres container  Docker network  ingestor ───► postgres  (host=postgres)`

TL;DR

* localhost inside a container = **that container**

* Port mapping = **PC ↔ container only**

* Container ↔ container:

  * Same Docker network

  * Use **service/container name**, not localhost

* Ingestion scripts should **never use localhost** to reach another container

One-Liner to Remember
> **If it’s inside Docker, localhost is almost always wrong.**

## Docker run command 

```bash
docker run -it --rm 
--network=pipeline_default \
taxi_ingest:v001 \
--pg-user=root \
--pg-pass=root \
--pg-host=pgdatabase \
--pg-port=5432 \
--pg-db=ny_taxi \
--target-table=yellow_taxi_trips \
--year=2021 \
--month=1 \
--chunksize=100000
```
