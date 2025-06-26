# Shiva Project Documentation

## Overview

**Shiva** is a modern, async Python framework for distributed systems and microservices. It provides a modular architecture for building scalable, event-driven applications, supporting protocols like RMQ, web APIs, metrics, and more. Shiva is built around the concept of **dispatchers**, **protocols**, **workers**, and **drivers**, enabling flexible orchestration of background tasks, message processing, and service integration.

## INSTALLATION

To install Shiva, simply run:

```bash
pip install shivad
```

---

## Core Concept: Dispatcher → Protocol → Workers + Drivers

- **Dispatcher**: Orchestrates the flow of messages or tasks. Each dispatcher is responsible for managing a set of workers and is configured to use a specific protocol and connection/driver.
- **Protocol**: Defines how messages are routed and processed between the dispatcher and its workers. Protocols can implement custom logic for message dispatching, serialization, and routing.
- **Workers**: Perform the actual business logic, such as processing messages, handling HTTP requests, or collecting metrics. Workers are instantiated and managed by dispatchers.
- **Drivers**: Abstract the connection to external systems (databases, message brokers, etc.). Each driver implements a standard interface for connecting, preparing, and stopping.

**Flow Example**:  
A dispatcher (e.g., RMQ) receives a message, uses a protocol (e.g., JSON_Routed_BPM) to determine which worker should handle it, and the worker processes the message, possibly using a driver (e.g., Postgres) to interact with a database.

---

## Project Structure and Main Components

```
shiva/
  common/         # Core abstractions (base classes, config, CLI, dispatcher logic)
  commands/       # CLI commands (Typer-based)
  dispatchers/    # Dispatcher implementations (RMQ, web, metrics, daemon)
  drivers/        # Drivers for databases, ESB, APIs
  proto/          # Protocols for message routing/handling
  workers/        # Example and real workers (metrics, web, daemon, etc.)
  examples/       # Example workers and usage
  lib/            # Utilities (config loader, tools)
  main.py         # FastAPI app entrypoint
  run.py          # CLI entrypoint
  shiva_cli.py    # CLI loader
```

---

## Public Classes, Functions, and Modules

### Core Abstractions

#### `BaseDispatcher`
- Manages a group of workers, applies a policy for worker instantiation, and handles lifecycle events (`prepare`, `start`, `stop`).
- Configurable via YAML: `name`, `coro`, `policy`, `connection`, `proto`, etc.

#### `BaseWorker`, `BaseDaemon`, `BaseRmqWorker`, `BaseMetric`
- Base classes for different worker types (generic, daemon, RMQ, metrics).
- Implement `prepare`, `start`, `stop` methods.

#### `BaseDriver`
- Abstracts connection to external systems (databases, ESB, APIs).
- Methods: `prepare`, `stop`.

#### `BaseProtocol`
- Handles message routing and dispatching logic between dispatcher and workers.

---

### Dispatchers

- **RMQ Dispatcher** (`shiva/dispatchers/rmq.py`): Handles RabbitMQ message consumption, manages exchanges/queues, and dispatches messages to workers via protocol.
- **Web Dispatcher** (`shiva/dispatchers/web.py`): Integrates FastAPI routers from workers, mounts them to the main app.
- **DaemonRoot** (`shiva/dispatchers/daemon.py`): Manages daemon-style workers (background loops).
- **MetricsRoot** (`shiva/dispatchers/metrics.py`): Exposes Prometheus metrics endpoints and manages metric workers.

---

### Protocols

- **JSON_UnroutedALL** (`shiva/proto/rmq_simple.py`): Simple protocol that dispatches all messages to all workers.
- **RoutedPublisher** (`shiva/proto/bpm.py`): Publishes messages with routing keys and metadata.

---

### Drivers

- **Postgres** (`shiva/drivers/databases/postgres.py`): Asyncpg-based connection pool.
- **Redis** (`shiva/drivers/databases/redis.py`): Aioredis-based connection pool.
- **MongoDB** (`shiva/drivers/databases/mongodb.py`): Motor-based async MongoDB client.
- **S3** (`shiva/drivers/api/s3_aiobotocore.py`): Async S3 client using aiobotocore.

---

### Example Workers

- **RMQ Worker** (`shiva/examples/workers/benchmark/rmq_bench.py`): Benchmarks RMQ message handling.
- **Daemon Worker** (`shiva/examples/workers/mydaemon/daemon_1.py`): Simple background loop.
- **Web Healthcheck** (`shiva/examples/workers/web/healthcheck.py`): FastAPI endpoints for readiness/liveness.
- **Metrics Worker** (`shiva/workers/metrics/some_metrics.py`): Prometheus metrics example.

---

## Usage Examples

### RMQ Worker Example

```python
from shiva.common.base import BaseRmqWorker
from shiva.common.rmq_routing import Router

router = Router()

class RmqBench(BaseRmqWorker):
    name = 'shiva_benchmark'
    dispatcher = 'shiva_bench'

    async def prepare(self):
        pass

    @router.route('shiva.bench')
    async def bench(self, message, raw=None):
        # Process message
        pass
```

### Simple Daemon Example

```python
from shiva.common.base import BaseDaemon

class MyDaemon(BaseDaemon):
    name = 'first_shiva_daemon'

    async def start(self):
        self.running = True
        while self.running:
            # Do work
            await asyncio.sleep(5)
```

### API (Web) Worker Example

```python
from fastapi import APIRouter
from shiva.common.base import BaseWorker
from shiva.dispatchers.web import Web

router = APIRouter(prefix='')

class Healthcheck(BaseWorker):
    name = 'healthcheck'
    dispatcher = Web

    @router.get("/readiness")
    def read():
        return {"status": "ok"}
```

### Metrics Example

```python
from prometheus_client import Counter, Gauge
from shiva.common.base import BaseMetric

class MyMetric(BaseMetric):
    name = 'my_metric'
    dispatcher = 'metrics_main'

    async def start(self):
        g = Gauge('my_gauge_metric', 'Some metric')
        c = Counter('my_counter', 'test_counter')
        self.running = True
        while self.running:
            g.inc()
            c.inc(1.2)
            await asyncio.sleep(5)
```

---

## YAML Configuration Reference

### Top-Level Structure

```yaml
app_name: shiva_test

common:
  uvloop: True
  coro_num: 1
  modules_path: './modules'

logging:
  level: DEBUG
  sentry:
    dsn: <sentry_dsn>
    environment: 'LOCAL'

connections:
  postgres:
    driver: postgres
    config:
      dsn: postgresql://postgres:@127.0.0.1:5432/mydb
      pool_min: 1
      pool_max: 50
      max_inactive_connection_lifetime: 300
      max_queries: 20
  redis:
    driver: redis
    config:
      dsn: redis://127.0.0.1:6379/0
      minsize: 1
      maxsize: 1
  rmq_default:
    driver: rmq
    config:
      dsn: amqp://guest:guest@127.0.0.1:5672/myvenv

dispatchers:
  web:
    name: web
    dispatcher: dispatcher_web
    enabled: true
  daemon_root_main:
    name: daemon_root_main
    dispatcher: daemon_root
    enabled: true
    policy: CONFIG
    coro: 1
    config:
      echo: I'm alive!
  shiva_bench:
    name: shiva_bench
    dispatcher: rmq
    connection: rmq_default
    proto: JSON_Routed_BPM
    enabled: false
    coro: 1
    config:
      exchanges:
        ESB:
          config:
            type: topic
            durable: true
          queues:
            shiva_benchmark:
              coro: 5
              config:
                prefetch: 1
                arguments:
                  auto_delete: false
                  durable: true
                additional:
                  max-length: 1000
              bindings:
                - shiva.bench

workers:
  waiter_daemon:
    name: waiter1
    coro: 1
    enabled: true
    worker: waiter_daemon
    dispatcher: daemon_root_main
    config:
      echo: Hello!
    depends:
      databases:
        - postgres
      esb:
        - rmq
```

#### Key Parameters

- **common**: General settings (uvloop, coroutine count, modules path)
- **logging**: Log level, Sentry integration
- **connections**: Database/message broker connections (driver, DSN, pool settings)
- **dispatchers**: Dispatcher instances (type, connection, protocol, policy, coroutines, config)
- **workers**: Worker instances (name, coroutines, enabled, worker class, dispatcher, config, dependencies)

#### Example: RMQ Dispatcher Section

```yaml
shiva_bench:
  name: shiva_bench
  dispatcher: rmq
  connection: rmq_default
  proto: JSON_Routed_BPM
  enabled: false
  coro: 1
  config:
    exchanges:
      ESB:
        config:
          type: topic
          durable: true
        queues:
          shiva_benchmark:
            coro: 5
            config:
              prefetch: 1
              arguments:
                auto_delete: false
                durable: true
              additional:
                max-length: 1000
            bindings:
              - shiva.bench
```

#### Example: Worker Section

```yaml
waiter_daemon:
  name: waiter1
  coro: 1
  enabled: true
  worker: waiter_daemon
  dispatcher: daemon_root_main
  config:
    echo: Hello!
  depends:
    databases:
      - postgres
    esb:
      - rmq
```

---

## Architecture Notes

- **Modular**: All major components (dispatchers, drivers, workers, protocols) are pluggable and discoverable via scopes.
- **Async**: Built on asyncio, supports uvloop for performance.
- **Config-Driven**: Most behavior is controlled via YAML configuration.
- **CLI**: Typer-based CLI for project management and running daemons.
- **Web**: FastAPI for web endpoints, Prometheus for metrics.

---

## Dependencies

- **Core**: FastAPI, Uvicorn, aiomisc, aio-pika, aioredis, asyncpg, PyYAML, orjson, loguru, sentry-sdk, flatdict, typer, art, marshmallow, motor, aiobotocore, prometheus-client, mako, starlette, fastapi-utils.
- **Dev**: ipython (optional).

---

## Conventions

- **Naming**: Dispatcher, worker, and driver names must match between code and YAML.
- **Workers**: Should inherit from the appropriate base class and register themselves with a dispatcher.
- **Protocols**: Should inherit from `BaseProtocol` and implement `dispatch`.
- **Drivers**: Should inherit from `BaseDriver` and implement `prepare` and `stop`.

---

## CLI Tools for Shiva

- **Entry Point**: `shiva` (see `pyproject.toml` and `shiva_cli.py`)
- **Adding Commands**: Use Typer in `shiva/commands/` modules.

### Example CLI Command

```python
import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    """Say hello."""
    print(f"Hello, {name}!")

if __name__ == "__main__":
    app()
```

- Add your command module to `shiva/commands/` and ensure it is loaded via `CommandHelper`.

---

## Running and Testing

- **Run the main app**:  
  ```bash
  python shiva/run.py
  ```
  or via CLI:
  ```bash
  shiva daemon run
  ```

- **Configuration**:  
  Set `SHIVA_CONFIG` env variable or use `./config.yml`.

- **Tests**:  
  There are example test commands in `shiva/commands/test.py`.  
  To run:
  ```bash
  python -m shiva.commands.test test
  ```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**End of Documentation**
