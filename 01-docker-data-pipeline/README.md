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
