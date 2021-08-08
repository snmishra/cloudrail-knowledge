
class DiagnosticLogs:

    def __init__(self, detailed_error_logging_enabled: bool, http_logging_enabled: bool, request_tracing_enabled: bool) -> None:
        self.detailed_error_logging_enabled: bool = detailed_error_logging_enabled
        self.http_logging_enabled: bool = http_logging_enabled
        self.request_tracing_enabled: bool = request_tracing_enabled

