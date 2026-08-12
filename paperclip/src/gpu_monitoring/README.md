# gpu_monitoring

GPU usage and monitoring

## Overview

This is an independent capability module in the Paperclip system.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

```python
from src.gpu_monitoring import GpuMonitoring

module = GpuMonitoring()
result = module.execute("task description")
```

## Configuration

Edit `config.yaml` to enable/disable this module:

```yaml
capabilities:
  gpu_monitoring: true  # or false to disable
```

## Testing

```bash
pytest tests/gpu_monitoring/
```
