import enum


class ProcessState(enum.Enum):
    CREATED = 0
    PROCESSING = 1
    PROCESSED = 2
    FAILED = 3
