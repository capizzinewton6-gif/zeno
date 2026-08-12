# restart_control

System restart control

## Overview

This is an independent capability module in the Paperclip system.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

```python
from src.restart_control import RestartControl

module = RestartControl()
result = module.execute("task description")
```

## Configuration

Edit `config.yaml` to enable/disable this module:

```yaml
capabilities:
  restart_control: true  # or false to disable
```

## Testing

```bash
pytest tests/restart_control/
```
