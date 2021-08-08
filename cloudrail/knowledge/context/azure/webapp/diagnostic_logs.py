from dataclasses import dataclass


@dataclass
class DiagnosticLogs:
    detailed_error_logging_enabled: bool
    http_logging_enabled: bool
    request_tracing_enabled: bool

