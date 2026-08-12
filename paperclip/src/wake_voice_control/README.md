# wake_voice_control

Wake on voice command

## Overview

This is an independent capability module in the Paperclip system.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

```python
from src.wake_voice_control import WakeVoiceControl

module = WakeVoiceControl()
result = module.execute("task description")
```

## Configuration

Edit `config.yaml` to enable/disable this module:

```yaml
capabilities:
  wake_voice_control: true  # or false to disable
```

## Testing

```bash
pytest tests/wake_voice_control/
```
