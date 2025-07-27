"""
Compatibility layer for testing on regular Python vs MicroPython
"""
import sys
import time as _time

# Check if we're running on MicroPython
try:
    import micropython
    IS_MICROPYTHON = True
except ImportError:
    IS_MICROPYTHON = False

# Time compatibility
if IS_MICROPYTHON:
    # Use MicroPython's time functions
    ticks_ms = _time.ticks_ms
    ticks_diff = _time.ticks_diff
    sleep_ms = _time.sleep_ms
else:
    # Emulate MicroPython time functions for regular Python
    def ticks_ms():
        """Emulate MicroPython's ticks_ms()"""
        return int(_time.time() * 1000)
    
    def ticks_diff(new, old):
        """Emulate MicroPython's ticks_diff()"""
        return new - old
    
    def sleep_ms(ms):
        """Emulate MicroPython's sleep_ms()"""
        _time.sleep(ms / 1000.0)

# Asyncio compatibility
try:
    import asyncio
    
    if not IS_MICROPYTHON:
        # For regular Python, ensure we have sleep_ms in asyncio
        if not hasattr(asyncio, 'sleep_ms'):
            async def sleep_ms(ms):
                await asyncio.sleep(ms / 1000.0)
            asyncio.sleep_ms = sleep_ms
    else:
        # MicroPython asyncio already has sleep_ms
        pass
        
except ImportError:
    # Fallback if asyncio not available
    class MockAsyncio:
        @staticmethod
        async def sleep_ms(ms):
            sleep_ms(ms)
        
        @staticmethod
        def Queue(maxsize=0):
            return []
    
    asyncio = MockAsyncio()

# Export the compatibility functions
__all__ = ['ticks_ms', 'ticks_diff', 'sleep_ms', 'IS_MICROPYTHON', 'asyncio']