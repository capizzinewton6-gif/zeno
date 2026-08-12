# ip_lookup

IP address lookup and geolocation

## Overview

This is an independent capability module in the Paperclip system.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

```python
from src.ip_lookup import IpLookup

module = IpLookup()
result = module.execute("task description")
```

## Configuration

Edit `config.yaml` to enable/disable this module:

```yaml
capabilities:
  ip_lookup: true  # or false to disable
```

## Testing

```bash
pytest tests/ip_lookup/
```
