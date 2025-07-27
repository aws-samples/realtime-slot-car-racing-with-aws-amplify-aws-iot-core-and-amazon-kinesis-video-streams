# boot.py - runs on every boot (before main.py)
# Raspberry Pi Pico 2 W Race Controller Boot Configuration

import gc
import machine

# Enable garbage collection
gc.enable()

# Set CPU frequency for optimal performance
machine.freq(133000000)  # 133MHz - good balance of performance and power

# Configure watchdog timer for system reliability
from machine import WDT
wdt = WDT(timeout=30000)  # 30 second watchdog

print("=== Pico 2 W Race Controller Boot ===")
print(f"CPU Frequency: {machine.freq()} Hz")
print(f"Free Memory: {gc.mem_free()} bytes")
print("Boot sequence complete")

# Feed watchdog to prevent reset during boot
wdt.feed()