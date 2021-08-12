from dataclasses import dataclass



@dataclass
class DiagnosticLogs:
    """
            Attributes:
                detailed_error_logging_enabled: Indicate if the detailed error logging enable or disable.
                http_logging_enabled: Indicate if the http logging enable or not.
                request_tracing_enabled: Indicate if the request tracing logging enable or not.
    """
    detailed_error_logging_enabled: bool
    http_logging_enabled: bool
    request_tracing_enabled: bool
