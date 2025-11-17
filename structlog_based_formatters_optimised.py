"""Test structlog with structlog-based formatters within logging (ProcessorFormatter) - OPTIMISED."""

import logging
import sys
import timeit

import orjson
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

# Configure structlog with optimizations:
# - Use make_filtering_bound_logger for efficient level filtering
# - Cache logger on first use
# Note: This still uses stdlib integration via ProcessorFormatter, but optimizes what we can
structlog.configure(
    cache_logger_on_first_use=True,
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    processors=[
        # Prepare event dict for `ProcessorFormatter`.
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

# Configure stdlib logging with ProcessorFormatter
# Use JSONRenderer with orjson instead of ConsoleRenderer for better performance
formatter = structlog.stdlib.ProcessorFormatter(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(serializer=orjson.dumps),
    ]
)

handler = logging.StreamHandler()
# Use OUR `ProcessorFormatter` to format all `logging` entries.
handler.setFormatter(formatter)
root_logger = logging.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)

# Setup loggers
struct_logger = structlog.get_logger()
stdlib_logger = logging.getLogger()

# Time structlog
print("Timing structlog (optimised)...", file=original_stdout)
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
