# lock_control

Screen lock control

## Overview

This is an independent capability module in the Paperclip system.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

```python
from src.lock_control import LockControl

module = LockControl()
result = module.execute("task description")
```

## Configuration

Edit `config.yaml` to enable/disable this module:

```yaml
capabilities:
  lock_control: true  # or false to disable
```

## Testing

```bash
pytest tests/lock_control/
```
