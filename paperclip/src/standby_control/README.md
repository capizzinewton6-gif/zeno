# standby_control

Standby mode control

## Overview

This is an independent capability module in the Paperclip system.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

```python
from src.standby_control import StandbyControl

module = StandbyControl()
result = module.execute("task description")
```

## Configuration

Edit `config.yaml` to enable/disable this module:

```yaml
capabilities:
  standby_control: true  # or false to disable
```

## Testing

```bash
pytest tests/standby_control/
```
