"""Test structlog and stdlib logging without integration."""

import logging
import sys
import timeit

import structlog


class NullIO:
    """A file-like object that discards all writes"""

    def write(self, *args, **kwargs):
        pass

    def flush(self, *args, **kwargs):
        pass

    def close(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


# Save original stdout for printing results
original_stdout = sys.stdout

# Replace stdout and stderr with null I/O
sys.stdout = NullIO()
sys.stderr = NullIO()

# Setup structlog (default configuration)
struct_logger = structlog.get_logger()

# Setup stdlib logging
stdlib_logger = logging.getLogger()

# Time structlog
print("Timing structlog...", file=original_stdout)
structlog_time = timeit.timeit(
    'struct_logger.info("Hello World!")', globals=globals(), number=100000
)
print(
    f"structlog: {structlog_time:.4f}s for 100000 calls ({structlog_time / 100000 * 1e6:.2f}μs per call)",
    file=original_stdout,
)

# Time stdlib
print("\nTiming stdlib...", file=original_stdout)
stdlib_time = timeit.timeit('stdlib_logger.info("Hello World!")', globals=globals(), number=100000)
print(
    f"stdlib: {stdlib_time:.4f}s for 100000 calls ({stdlib_time / 100000 * 1e6:.2f}μs per call)",
    file=original_stdout,
)
