# wikipedia_search

Wikipedia search and article retrieval

## Overview

This is an independent capability module in the Paperclip system.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

```python
from src.wikipedia_search import WikipediaSearch

module = WikipediaSearch()
result = module.execute("task description")
```

## Configuration

Edit `config.yaml` to enable/disable this module:

```yaml
capabilities:
  wikipedia_search: true  # or false to disable
```

## Testing

```bash
pytest tests/wikipedia_search/
```
