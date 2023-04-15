from enum import Enum


class InvocationStatus(Enum):
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    FAILED = "FAILED"
