"""
Structured JSON logging configuration for the Semantic Analysis Backend.
Integrates with the ELK stack (Elasticsearch, Logstash, Kibana) by producing
JSON-formatted log output that Filebeat/Logstash can ingest directly.
"""
import logging
import sys
from pythonjsonlogger import json as jsonlogger


def setup_logging(service_name: str = "semantic-backend", level: str = "INFO") -> logging.Logger:
    """
    Configure and return a structured JSON logger.
    
    All log entries include:
      - timestamp, level, message (standard)
      - service, environment (contextual)
    
    Additional fields can be passed as `extra={}` on each log call.
    """
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Prevent duplicate handlers on re-import
    if logger.handlers:
        return logger

    # JSON formatter for structured log output
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        rename_fields={
            "asctime": "timestamp",
            "name": "service",
            "levelname": "level",
        },
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    # Console handler (stdout → captured by Docker/K8s log drivers)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Prevent propagation to root logger (avoids plain-text duplicates)
    logger.propagate = False

    return logger
