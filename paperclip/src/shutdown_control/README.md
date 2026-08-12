# shutdown_control

System shutdown control

## Overview

This is an independent capability module in the Paperclip system.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

```python
from src.shutdown_control import ShutdownControl

module = ShutdownControl()
result = module.execute("task description")
```

## Configuration

Edit `config.yaml` to enable/disable this module:

```yaml
capabilities:
  shutdown_control: true  # or false to disable
```

## Testing

```bash
pytest tests/shutdown_control/
```
