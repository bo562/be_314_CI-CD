'''
This class is used to store basic states that a database object may be in, including Connected, Stale, Disconnected, Error
'''

from enum import Enum

class DatabaseStatus(Enum):
    NoImplemented = -1
    Connected = 0
    Disconnected = 1
    Stale = 2
    Error = 3