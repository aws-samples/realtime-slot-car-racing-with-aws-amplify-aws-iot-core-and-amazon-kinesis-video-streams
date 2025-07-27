"""
Simple logging module for MicroPython
"""
import config
from compat import ticks_ms

class Logger:
    """Simple logger for debugging race controller"""
    
    def __init__(self, name="RaceController"):
        """Initialize logger with name"""
        self.name = name
        self.level = config.LOG_LEVEL
    
    def _log(self, level, level_name, message):
        """Internal logging method"""
        if level >= self.level:
            timestamp = ticks_ms()
            print(f"[{timestamp}] {level_name} {self.name}: {message}")
    
    def debug(self, message):
        """Log debug message"""
        self._log(config.LOG_DEBUG, "DEBUG", message)
    
    def info(self, message):
        """Log info message"""
        self._log(config.LOG_INFO, "INFO", message)
    
    def warning(self, message):
        """Log warning message"""
        self._log(config.LOG_WARNING, "WARN", message)
    
    def error(self, message):
        """Log error message"""
        self._log(config.LOG_ERROR, "ERROR", message)

# Global logger instance
log = Logger()