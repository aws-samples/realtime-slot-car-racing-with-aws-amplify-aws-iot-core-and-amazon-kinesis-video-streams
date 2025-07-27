# Raspberry Pi Pico 2 W Race Controller (MicroPython)

This is a MicroPython refactor of the original RaspberryPythonRaceController, optimized for the Raspberry Pi Pico 2 W with improved reliability through asyncio and queuing.

## Features

- **Async/Await Architecture**: Uses MicroPython's asyncio for concurrent processing
- **Reliable Serial Communication**: Queued serial I/O with error handling
- **MQTT Integration**: AWS IoT Core connectivity with automatic reconnection
- **Modular Design**: Clean separation of concerns with proper classes
- **Comprehensive Logging**: Debug-friendly logging system
- **Race State Management**: Full race lifecycle support
- **Lap Time Tracking**: Accurate lap time detection and reporting

## Hardware Requirements

### Raspberry Pi Pico 2 W
- Raspberry Pi Pico 2 W (RP2350 with WiFi)
- MicroPython firmware 1.20.0 or later

### USB-A Breakout Board
For serial communication with the race track, you'll need a **USB-A Female Breakout Board**:

**Recommended**: 
- **Adafruit USB Type A Female Breakout Board** (Product ID: 1833)
- **SparkFun USB Type A Female Breakout** (BOB-12700)
- **Generic USB-A Female to 4-pin header breakout**

**Connections**:
```
USB-A Breakout → Pico 2 W
VCC (5V)       → VBUS (Pin 40)
D- (Data-)     → GP0 (Pin 1) - UART TX
D+ (Data+)     → GP1 (Pin 2) - UART RX  
GND            → GND (Pin 38)
```

### Race Track Connection
- Scalextric or compatible slot car track
- Track controller with USB output
- USB cable to connect track controller to USB-A breakout

## Software Setup

### 1. Install MicroPython
Flash MicroPython firmware to your Pico 2 W:
1. Download latest MicroPython firmware for Pico 2 W
2. Hold BOOTSEL button while connecting USB
3. Copy firmware .uf2 file to RPI-RP2 drive

### 2. Install Required Libraries
Copy these libraries to your Pico 2 W:
```python
# Required MicroPython libraries
import network      # Built-in WiFi
import asyncio      # Built-in async support
import json         # Built-in JSON
import ssl          # Built-in SSL
from umqtt.simple import MQTTClient  # Install via upip
```

Install umqtt:
```python
import upip
upip.install('micropython-umqtt.simple')
```

### 3. Configuration
Edit `config.py` with your settings:

```python
# WiFi Configuration
WIFI_SSID = "your_wifi_network"
WIFI_PASSWORD = "your_wifi_password"

# AWS IoT Core Configuration  
AWS_IOT_ENDPOINT = "your-endpoint-ats.iot.region.amazonaws.com"
AWS_IOT_CLIENT_ID = "pico2w-race-controller"

# Serial Configuration
UART_TX_PIN = 0  # GP0 for USB D-
UART_RX_PIN = 1  # GP1 for USB D+
UART_BAUDRATE = 19200
```

### 4. AWS IoT Core Setup
1. Create an IoT Thing in AWS IoT Core
2. Generate certificates and download:
   - Certificate file (.pem.crt)
   - Private key file (.pem.key)  
   - Root CA certificate
3. Create IoT policy with required permissions
4. Update `config.py` with your endpoint

## File Structure

```
RaspberryPythonRaceController_mpy/
├── main.py              # Main application entry point
├── config.py            # Configuration settings
├── logger.py            # Logging utilities
├── wifi_manager.py      # WiFi connection management
├── mqtt_client.py       # AWS IoT Core MQTT client
├── serial_client.py     # Serial communication with track
├── race_controller.py   # Main race logic
├── models.py            # Data models (Car, LapTime, etc.)
├── byte_helper.py       # Byte manipulation utilities
├── tests/               # Test scripts
│   ├── test_byte_helper.py
│   ├── test_models.py
│   ├── test_race_controller.py
│   └── run_all_tests.py
└── README.md           # This file
```

## Usage

### Running the Application
1. Copy all files to your Pico 2 W
2. Configure `config.py` with your settings
3. Run the main application:
```python
import main
# Application will start automatically
```

### Testing
Run the test suite to validate functionality:
```python
import tests.run_all_tests
```

### Monitoring
The application provides detailed logging. Set log level in `config.py`:
```python
LOG_LEVEL = LOG_DEBUG  # For detailed debugging
LOG_LEVEL = LOG_INFO   # For normal operation
```

## Architecture

### Async Processing
The application uses asyncio for concurrent processing:
- **MQTT Message Processor**: Handles incoming race/car updates
- **Serial Data Processor**: Processes track data
- **Track Update Sender**: Sends control commands to track
- **Lap Time Sender**: Publishes lap times to MQTT
- **Analytics Sender**: Publishes race analytics
- **Status Monitor**: Monitors connections and reconnects

### Queuing System
Reliable communication through asyncio queues:
- **Serial Send Queue**: Outgoing track commands
- **Serial Receive Queue**: Incoming track data
- **MQTT Publish Queue**: Outgoing MQTT messages
- **MQTT Message Queue**: Incoming MQTT messages
- **Lap Times Queue**: Detected lap times
- **Analytics Queue**: Race analytics data

### Error Handling
- Automatic WiFi reconnection
- MQTT connection recovery
- Serial communication error handling
- Queue overflow protection
- Comprehensive logging

## MQTT Topics

### Subscribed Topics
- `GAME_STATE_UPDATE`: Race state changes
- `CAR_CONTROL_UPDATE`: Car throttle/control updates
- `6cpb/incoming`: Track data (if using MQTT for track)

### Published Topics
- `RACE_LAP_TIME`: Lap time records
- `RACE_ANALYTICS`: Race analytics data
- `6cpb/outgoing`: Track commands (if using MQTT for track)

## Troubleshooting

### Common Issues

1. **WiFi Connection Failed**
   - Check SSID/password in config.py
   - Verify WiFi network is 2.4GHz (Pico 2 W doesn't support 5GHz)
   - Check signal strength

2. **MQTT Connection Failed**
   - Verify AWS IoT endpoint URL
   - Check certificates are properly installed
   - Ensure IoT policy allows required actions

3. **Serial Communication Issues**
   - Verify USB-A breakout wiring
   - Check UART pin configuration
   - Ensure correct baudrate (19200)
   - Test with multimeter for signal levels

4. **Memory Issues**
   - MicroPython has limited RAM
   - Reduce queue sizes in code if needed
   - Monitor memory usage with `gc.mem_free()`

### Debug Mode
Enable debug logging for detailed troubleshooting:
```python
# In config.py
LOG_LEVEL = LOG_DEBUG
```

## Performance Considerations

- **Queue Sizes**: Configured for optimal memory usage
- **Timing**: Refresh rates optimized for responsiveness
- **Memory Management**: Automatic garbage collection
- **Connection Pooling**: Efficient MQTT/WiFi management

## Differences from Original

### Improvements
- ✅ Async/await architecture vs threading
- ✅ Proper error handling and recovery
- ✅ Modular, testable code structure
- ✅ Comprehensive logging system
- ✅ Queue-based communication
- ✅ Memory-efficient design

### Limitations
- ⚠️ MicroPython has less library support
- ⚠️ Limited RAM compared to full Python
- ⚠️ No GUI support (console only)
- ⚠️ Simplified SSL/TLS implementation

## Contributing

1. Run tests before submitting changes
2. Follow MicroPython coding conventions
3. Update documentation for new features
4. Test on actual hardware when possible

## License

Same as original project - MIT-0 License