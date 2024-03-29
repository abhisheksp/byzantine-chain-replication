from enum import Enum


class Mode(Enum):
    ACTIVE = 1
    PENDING = 2
    IMMUTABLE = 3

REPLICA_PORT = 9002