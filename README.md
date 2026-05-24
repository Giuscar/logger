# Python Custom Logger

Python Custom Logger is a small wrapper around Python's standard `logging`
library. It provides a consistent log format for applications that need readable
text logs or structured JSON logs without repeating formatter setup in every
module.

## What This Repository Contains

This repository contains:

- `custom_logger.CustomLogger`: a logger wrapper with convenience methods such
  as `debug`, `info`, `warning`, `error`, `critical`, and `exception`.
- `custom_logger.CustomFormatter`: a formatter that outputs logs as plain text
  or JSON.
- `custom_logger.get_logger`: a helper function that returns a configured
  `CustomLogger` instance.
- Unit tests covering formatter behavior, logger levels, text output, JSON
  output, and integration examples.

## Features

- Formats dates as `yyyy-mm-dd`.
- Formats times as `hh:mm:ss`.
- Includes the logger name.
- Includes the calling function name when the log call comes from a function or
  method.
- Supports both `text` and `json` output.
- Allows custom logging levels and custom handlers.
- Uses Python's built-in `logging` module, so it stays lightweight and familiar.

## Example Text Output

```text
2006-02-08 22:20:02 fbloggsfunction sample_method Protocol problem: connection reset
```

## Example JSON Output

```json
{
  "date": "2006-02-08",
  "time": "22:20:02",
  "name": "fbloggsfunction",
  "message": "Protocol problem: connection reset",
  "funcName": "sample_method"
}
```

## Usage

```python
from custom_logger import CustomLogger

logger = CustomLogger(name="fbloggsfunction", format="text")
logger.info("Protocol problem: connection reset")
```

JSON output can be enabled by changing the `format` argument:

```python
from custom_logger import get_logger

logger = get_logger(name="fbloggsfunction", format="json")
logger.warning("Connection is slow")
```

## Running The Example

```bash
python3 example.py
```

## Running Tests

Install the development dependencies, then run the test suite with `pytest`:

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest tests/test_custom_logger.py
```
