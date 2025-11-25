# Cogito

![Build Status](https://github.com/benballintyn/cogito/actions/workflows/run_tests.yml/badge.svg?branch=main)
![Coverage](https://img.shields.io/endpoint?url=https://benballintyn.github.io/cogito/coverage.json)
![License](https://img.shields.io/github/license/benballintyn/cogito)
![Python Version](https://img.shields.io/pypi/pyversions/cogito)

Cogito is a collection of robust Python utilities designed to simplify common development tasks. It includes tools for API interaction, asynchronous retries, JSONLines processing, and more.

## Installation

You can install `cogito` using pip:

```bash
pip install cogito
```

Or with Poetry:

```bash
poetry add cogito
```

## Features

- **APIClient**: A wrapper around `httpx` for making HTTP requests with built-in error handling and rate limiting.
- **Async Retry**: A decorator for retrying asynchronous functions with exponential backoff.
- **JSONLines**: Utilities for reading and writing JSONLines files.
- **Dynamic Importer**: Helper functions for dynamically importing modules and classes.

## Usage

### APIClient

```python
import asyncio
from cogito.utils.api_client import APIClient

class MyAPI(APIClient):
    def __init__(self):
        super().__init__(base_url="https://api.example.com")

async def main():
    api = MyAPI()
    response = await api.get("/data")
    print(response.json())

if __name__ == "__main__":
    asyncio.run(main())
```

### Async Retry

```python
import asyncio
from cogito.utils.retry import async_retry

@async_retry(max_retries=3, backoff_factor=0.5)
async def fetch_data():
    # ... some async operation that might fail ...
    pass
```

### JSONLines

```python
from cogito.utils.jsonlines import read_jsonl, write_jsonl

data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
write_jsonl("users.jsonl", data)

users = list(read_jsonl("users.jsonl"))
print(users)
```

## Development

To contribute to `cogito`, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/benballintyn/cogito.git
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

3. Run tests:
   ```bash
   poetry run pytest
   ```