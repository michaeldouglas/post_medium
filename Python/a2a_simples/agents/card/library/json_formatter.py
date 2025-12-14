import json
import logging
import time
import os


class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),

            # correlação
            "request_id": getattr(record, "request_id", "-"),
            "task_id": getattr(record, "task_id", None),
            "message_id": getattr(record, "message_id", None),

            # contexto
            "service": os.getenv("SERVICE_NAME", "unknown"),
            "env": os.getenv("ENV", "local"),

            # semântica
            "event": getattr(record, "event", None),
            "agent": getattr(record, "agent", None),
            "skill": getattr(record, "skill", None),

            # performance
            "duration_ms": getattr(record, "duration_ms", None),
        }

        # campos HTTP (middleware)
        for field in ("method", "path", "status_code", "client"):
            value = getattr(record, field, None)
            if value is not None:
                log_record[field] = value

        # exceções
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record, ensure_ascii=False)
