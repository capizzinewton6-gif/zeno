# archive_management

Archive creation and extraction (ZIP, TAR, etc.)

## Overview

This is an independent capability module in the Paperclip system.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

```python
from src.archive_management import ArchiveManagement

module = ArchiveManagement()
result = module.execute("task description")
```

## Configuration

Edit `config.yaml` to enable/disable this module:

```yaml
capabilities:
  archive_management: true  # or false to disable
```

## Testing

```bash
pytest tests/archive_management/
```
