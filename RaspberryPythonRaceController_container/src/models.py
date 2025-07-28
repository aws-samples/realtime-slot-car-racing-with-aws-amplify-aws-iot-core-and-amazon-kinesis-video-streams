"""Data models for the race controller."""
import json
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class Car:
    """Represents a race car with its current state."""
    
    number: int
    player_id: str = ""
    throttle: int = 0
    lane_change_req: bool = False
    brakes_on_req: bool = False
    latest_finish_time: int = 0
    
    def __post_init__(self):
        """Validate car data after initialization."""
        if not 1 <= self.number <= 6:
            raise ValueError(f"Car number must be 1-6, got {self.number}")
        if not 0 <= self.throttle <= 100:
            raise ValueError(f"Throttle must be 0-100, got {self.throttle}")


@dataclass
class LapTime:
    """Represents a lap time record."""
    
    race_id: str
    player_id: str
    time_ms: int
    timestamp: Optional[float] = None
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = time.time()
    
    def to_json(self) -> str:
        """Convert to JSON string for MQTT publishing."""
        return json.dumps({
            'raceId': self.race_id,
            'playerId': self.player_id,
            'timeInMilliSec': self.time_ms,
            'timestamp': self.timestamp
        })
    
    def __str__(self) -> str:
        """String representation for logging."""
        return f"{self.race_id}:{self.player_id}:{self.time_ms}"


@dataclass
class RaceAnalytics:
    """Represents race analytics data."""
    
    race_id: str
    track_power_status: bool
    port_current: int
    active_cars: int
    timestamp: Optional[float] = None
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = time.time()
    
    def to_json(self) -> str:
        """Convert to JSON string for MQTT publishing."""
        return json.dumps({
            'raceId': self.race_id,
            'trackPowerStatus': self.track_power_status,
            'portCurrent': self.port_current,
            'activeCars': self.active_cars,
            'timestamp': self.timestamp
        })