import enum


class FailureStatus(enum.IntEnum):
    NoFailure = 0
    Failure = 1
    CriticalFailure = 2
    Expired = 3
