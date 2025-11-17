# Structlog Performance Benchmarks

Performance comparison of structlog vs stdlib logging across different integration methods.

All benchmarks run 100,000 log calls with I/O disabled (using NullIO) to measure pure processing overhead.

**Original notebook**: [testing_structlog.ipynb](testing_structlog.ipynb)

## Results

### 1. No Integration ([`no_integration.py`](no_integration.py))

- **structlog**: 10.14μs per call
- **stdlib**: 0.08μs per call

### 2. Rendering Within Structlog ([`rendering_within_structlog.py`](rendering_within_structlog.py))

- **structlog**: 59.31μs per call
- **stdlib**: 4.18μs per call

### 3. Logging-Based Formatters ([`logging_based_formatters.py`](logging_based_formatters.py))

- **structlog**: 1.04μs per call
- **stdlib**: 0.08μs per call

### 4. Structlog-Based Formatters ([`structlog_based_formatters.py`](structlog_based_formatters.py))

- **structlog**: 16.14μs per call
- **stdlib**: 11.37μs per call

## Running the Benchmarks

```bash
uv run python structlog_testing/no_integration.py
uv run python structlog_testing/rendering_within_structlog.py
uv run python structlog_testing/logging_based_formatters.py
uv run python structlog_testing/structlog_based_formatters.py
```
