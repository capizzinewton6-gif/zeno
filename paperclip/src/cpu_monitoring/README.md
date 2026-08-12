# cpu_monitoring

CPU usage and performance monitoring

## Overview

This is an independent capability module in the Paperclip system.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

```python
from src.cpu_monitoring import CpuMonitoring

module = CpuMonitoring()
result = module.execute("task description")
```

## Configuration

Edit `config.yaml` to enable/disable this module:

```yaml
capabilities:
  cpu_monitoring: true  # or false to disable
```

## Testing

```bash
pytest tests/cpu_monitoring/
```
