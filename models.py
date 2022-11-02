import dataclasses
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class AuthCredentials:
    admin_password: str
    participant_label: str

    def asdict(self) -> dict:
        return dataclasses.asdict(self)


@dataclass(frozen=True)
class RaspiConfig:
    test_mode: bool
    sample_wait: float
    send_rate: float
    gpio_pin: int
    mode: str
    no_output: bool

    def asdict(self) -> dict:
        return dataclasses.asdict(self)


@dataclass
class DataPoint:
    timestamp_enter: float
    timestamp_exit: float


class RecordingInstructions(Enum):
    START = 'start'
    PAUSE = 'pause'
    STOP = 'stop'
