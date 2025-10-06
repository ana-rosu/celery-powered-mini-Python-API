# Async Pi Calculator: FastAPI + Celery + Redis

This project is a Python web API that calculates n digits of π (pi) asynchronously using Celery and Redis.
It exposes two API endpoints via FastAPI:

`/calculate_pi?n=<number>` – start a background task to compute π <br>
`/check_progress?task_id=<id>` – check task progress and retrieve the result

## Features

- Asynchronous background computation using Celery
- Real-time progress tracking
- Lightweight FastAPI REST interface
- Redis used as message broker and result backend
- Fully containerized with Docker Compose

## Project Structure

```
app/
├── main.py          # Creates FastAPI app
├── routes.py        # Defines API endpoints
├── tasks.py         # Celery configuration + task definition
├── calculator.py    # Logic to compute π progressively
├── enums.py         # Enums containing task states
├── __init__.py      # Makes 'app' a Python package
Dockerfile           # Container build instructions
docker-compose.yml   # Runs FastAPI, Celery worker, and Redis together
README.md            # Project documentation and usage guide
```

## Running with Docker Compose

Make sure Docker and Docker Compose are installed on your system. If you don’t have Docker installed yet, follow the instructions [here](https://docs.docker.com/get-started/get-docker/).

Start everything (FastAPI, Celery worker, Redis) with a single command:

```
docker compose up --build
```

You should see logs from all services.

API will be available at http://localhost:8000.<br>
Swagger docs at http://localhost:8000/docs.

[Optional] Verify everything is running by checking the status of containers with `docker compose ps`. You should see fastapi, celery, and redis running.

To stop and remove the services:

```
docker compose down
```

<details>
<summary> Request/Response Examples</summary>

`GET /calculate_pi`

Example Request:

```
http://localhost:8000/calculate_pi?n=10
```

Example Response:

```
{
  "task_id": "d7eccb93-d06c-4f83-862d-3f14a3cda405"
}
```

`GET /check_progress`
Example Request:

```
http://localhost:8000/check_progress?task_id=d7eccb93-d06c-4f83-862d-3f14a3cda405
```

Example Responses:

- While running:

```
{
  "state": "PROGRESS",
  "progress": 0.25,
  "result": null
}
```

- When finished:

```
{
  "state": "FINISHED",
  "progress": 1.0,
  "result": 3.1415926535
}
```

  </details>

## How it works

```
Client → FastAPI → Celery Task enqueued → Redis (broker) → Celery Worker → Result stored in Redis
```

1. The `/calculate_pi` FastAPI endpoint (**producer**) enqueues a Celery task (`compute_pi`) using Redis (as the **message broker**).

2. The Celery worker (**consumer**) picks up the task and runs the calculation in the background, yielding intermediate progress.

3. Each progress update is stored in Redis (`self.update_state`).

4. The `/check_progress` endpoint queries Redis (through Celery’s API) for the task’s current state and returns its progress and result.

Redis acts as both:

- Broker – temporary message queue (tasks waiting to be picked up). <br>
- Backend – persistent store for progress & results.

---

This project is submitted for the JetBrains PostTagger reimagined project / Internship Task #1.
