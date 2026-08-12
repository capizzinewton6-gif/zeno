# application_launcher

Application launching by name or path

## Overview

This is an independent capability module in the Paperclip system.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

```python
from src.application_launcher import ApplicationLauncher

module = ApplicationLauncher()
result = module.execute("task description")
```

## Configuration

Edit `config.yaml` to enable/disable this module:

```yaml
capabilities:
  application_launcher: true  # or false to disable
```

## Testing

```bash
pytest tests/application_launcher/
```
