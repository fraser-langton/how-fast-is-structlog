# Structlog Performance Benchmarks

Performance comparison of structlog vs stdlib logging across different integration methods.

All benchmarks run 100,000 log calls with I/O disabled (using NullIO) to measure pure processing overhead.

**Original notebook**: [testing_structlog.ipynb](testing_structlog.ipynb)

## Results

https://www.structlog.org/en/stable/standard-library.html

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

## Optimised Results

https://www.structlog.org/en/stable/performance.html

Following [structlog performance recommendations](https://www.structlog.org/en/stable/performance.html):

### 1. No Integration ([`no_integration_optimised.py`](no_integration_optimised.py))

- **structlog**: 4.42μs per call (2.3x faster than original)
- **stdlib**: 0.08μs per call

### 2. Rendering Within Structlog ([`rendering_within_structlog_optimised.py`](rendering_within_structlog_optimised.py))

- **structlog**: 3.00μs per call (19.8x faster than original)
- **stdlib**: 4.22μs per call

### 3. Logging-Based Formatters ([`logging_based_formatters_optimised.py`](logging_based_formatters_optimised.py))

- **structlog**: 0.82μs per call (1.3x faster than original)
- **stdlib**: 0.08μs per call

### 4. Structlog-Based Formatters ([`structlog_based_formatters_optimised.py`](structlog_based_formatters_optimised.py))

- **structlog**: 15.61μs per call
- **stdlib**: 13.28μs per call

## Running the Benchmarks

### Standard Benchmarks

```bash
uv run python no_integration.py
uv run python rendering_within_structlog.py
uv run python logging_based_formatters.py
uv run python structlog_based_formatters.py
```

### Optimised Benchmarks

```bash
uv run python no_integration_optimised.py
uv run python rendering_within_structlog_optimised.py
uv run python logging_based_formatters_optimised.py
uv run python structlog_based_formatters_optimised.py
```
