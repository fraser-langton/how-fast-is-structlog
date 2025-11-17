"""Test structlog rendering within structlog (JSONRenderer) - OPTIMISED."""

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

    # BytesLogger uses sys.stdout.buffer, so we need a buffer attribute
    @property
    def buffer(self):
        return self


# Save original stdout for printing results
original_stdout = sys.stdout

# Replace stdout and stderr with null I/O
null_io = NullIO()
sys.stdout = null_io
sys.stderr = NullIO()

# Configure structlog with optimizations:
# - Use make_filtering_bound_logger for efficient level filtering
# - Use BytesLoggerFactory since orjson returns bytes (saves encoding overhead)
# - Use orjson for faster JSON serialization
# - Cache logger on first use
# - Removed CallsiteParameterAdder (it's slow - extracts stack traces)
# - Removed stdlib integration (use native structlog)
structlog.configure(
    cache_logger_on_first_use=True,
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    processors=[
        structlog.processors.add_log_level,
        # Add a timestamp in ISO 8601 format.
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        # If the "exc_info" key in the event dict is either true or a
        # sys.exc_info() tuple, remove "exc_info" and render the exception
        # with traceback into the "exception" key.
        structlog.processors.format_exc_info,
        # If some value is in bytes, decode it to a Unicode str.
        structlog.processors.UnicodeDecoder(),
        # Render the final event dict as JSON using orjson.
        structlog.processors.JSONRenderer(serializer=orjson.dumps),
    ],
    logger_factory=structlog.BytesLoggerFactory(),
)

# Configure stdlib logging
logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)

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
