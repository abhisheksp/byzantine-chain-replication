from enum import Enum


class Mode(Enum):
    ACTIVE = 1
    PENDING = 2
    IMMUTABLE = 3


class Type(Enum):
    HEAD = 1
    INTERNAL = 2
    TAIL = 3
