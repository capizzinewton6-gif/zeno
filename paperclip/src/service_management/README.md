# service_management

Start, stop, and manage system services

## Overview

This is an independent capability module in the Paperclip system.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

```python
from src.service_management import ServiceManagement

module = ServiceManagement()
result = module.execute("task description")
```

## Configuration

Edit `config.yaml` to enable/disable this module:

```yaml
capabilities:
  service_management: true  # or false to disable
```

## Testing

```bash
pytest tests/service_management/
```
