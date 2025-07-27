# Setup Guide - Raspberry Pi Pico 2 W Race Controller

## Hardware Setup

### 1. Raspberry Pi Pico 2 W Preparation

1. **Flash MicroPython Firmware**:
   - Download latest MicroPython firmware for Pico 2 W from micropython.org
   - Hold BOOTSEL button while connecting USB to PC
   - Copy .uf2 firmware file to RPI-RP2 drive
   - Device will reboot with MicroPython

2. **Verify Installation**:
   ```python
   >>> import sys
   >>> sys.implementation
   # Should show MicroPython version
   ```

### 2. USB-A Breakout Board Wiring

**Recommended Breakout Boards**:
- Adafruit USB Type A Female Breakout (ID: 1833) - $2.95
- SparkFun USB Type A Female Breakout (BOB-12700) - $1.95
- Generic USB-A female to pin header breakout

**Wiring Diagram**:
```
USB-A Breakout    Pico 2 W Pin    Function
--------------    ------------    --------
VCC (Red)         VBUS (40)       5V Power
D- (White)        GP0 (1)         UART0 TX
D+ (Green)        GP1 (2)         UART0 RX
GND (Black)       GND (38)        Ground
```

**Physical Connection**:
1. Solder pin headers to USB-A breakout board
2. Connect jumper wires as shown above
3. Use breadboard or perfboard for stable connections
4. Add 100nF capacitor between VCC and GND for noise filtering (optional)

### 3. Race Track Connection

1. **Track Controller**: Connect Scalextric track controller to USB-A breakout
2. **Power**: Ensure track has separate power supply
3. **Testing**: Use multimeter to verify 5V on VCC pin when track is powered

## Software Setup

### 1. File Transfer to Pico 2 W

**Using Thonny IDE** (Recommended):
1. Install Thonny IDE
2. Connect Pico 2 W via USB
3. Select "MicroPython (Raspberry Pi Pico)" interpreter
4. Copy all .py files to device using File → Save As → Raspberry Pi Pico

**Using ampy** (Command Line):
```bash
pip install adafruit-ampy
ampy --port /dev/ttyACM0 put main.py
ampy --port /dev/ttyACM0 put config.py
# ... repeat for all files
```

**Using rshell**:
```bash
pip install rshell
rshell --port /dev/ttyACM0
> cp *.py /pyboard/
```

### 2. Install Dependencies

Connect to Pico 2 W REPL and run:
```python
import network
import upip

# Connect to WiFi first
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('your_wifi_ssid', 'your_wifi_password')

# Wait for connection
while not wlan.isconnected():
    pass

# Install MQTT library
upip.install('micropython-umqtt.simple')
```

### 3. Configuration

Edit `config.py` with your specific settings:

```python
# WiFi Settings
WIFI_SSID = "YourWiFiNetwork"
WIFI_PASSWORD = "YourWiFiPassword"

# AWS IoT Core Settings
AWS_IOT_ENDPOINT = "your-endpoint-ats.iot.us-west-2.amazonaws.com"
AWS_IOT_CLIENT_ID = "pico2w-race-controller-001"

# Hardware Settings (adjust if needed)
UART_TX_PIN = 0  # GP0
UART_RX_PIN = 1  # GP1
UART_BAUDRATE = 19200
```

## AWS IoT Core Setup

### 1. Create IoT Thing

```bash
# Using AWS CLI
aws iot create-thing --thing-name "pico2w-race-controller"
```

### 2. Generate Certificates

```bash
# Create certificate
aws iot create-keys-and-certificate \
    --set-as-active \
    --certificate-pem-outfile cert.pem \
    --public-key-outfile public.key \
    --private-key-outfile private.key

# Note the certificate ARN from output
```

### 3. Create IoT Policy

Create policy file `race-controller-policy.json`:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:Connect",
        "iot:Publish",
        "iot:Subscribe",
        "iot:Receive"
      ],
      "Resource": "*"
    }
  ]
}
```

Apply policy:
```bash
aws iot create-policy \
    --policy-name "RaceControllerPolicy" \
    --policy-document file://race-controller-policy.json

aws iot attach-policy \
    --policy-name "RaceControllerPolicy" \
    --target "CERTIFICATE_ARN_FROM_STEP_2"
```

### 4. Attach Certificate to Thing

```bash
aws iot attach-thing-principal \
    --thing-name "pico2w-race-controller" \
    --principal "CERTIFICATE_ARN_FROM_STEP_2"
```

## Testing Setup

### 1. Hardware Test

```python
# Test UART communication
from machine import UART, Pin
uart = UART(0, baudrate=19200, tx=Pin(0), rx=Pin(1))

# Send test data
uart.write(b'\\x00\\x01\\x02\\x03')

# Check for received data
if uart.any():
    data = uart.read()
    print([hex(x) for x in data])
```

### 2. WiFi Test

```python
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('your_ssid', 'your_password')

# Wait and check
import time
time.sleep(10)
print("Connected:", wlan.isconnected())
print("IP:", wlan.ifconfig()[0])
```

### 3. MQTT Test

```python
from umqtt.simple import MQTTClient
import ssl

client = MQTTClient(
    client_id="test-client",
    server="your-endpoint-ats.iot.region.amazonaws.com",
    port=8883,
    ssl=True
)

try:
    client.connect()
    client.publish("test/topic", "Hello from Pico 2 W!")
    print("MQTT test successful")
except Exception as e:
    print("MQTT test failed:", e)
```

### 4. Run Full Test Suite

```python
import tests.run_all_tests
# Should show all tests passing
```

## Deployment

### 1. Final Configuration Check

Verify all settings in `config.py`:
- WiFi credentials correct
- AWS IoT endpoint correct
- UART pins match your wiring
- Log level appropriate for production

### 2. Auto-Start Setup

The application will auto-start when `main.py` is present. For manual control:

```python
# To start manually
import main

# To stop (Ctrl+C in REPL)
# Then restart with soft reset: Ctrl+D
```

### 3. Monitoring

Connect to REPL to monitor operation:
```python
# Check memory usage
import gc
print("Free memory:", gc.mem_free())

# Check WiFi status
import network
wlan = network.WLAN(network.STA_IF)
print("WiFi connected:", wlan.isconnected())
```

## Troubleshooting

### Common Issues

1. **"ImportError: no module named 'umqtt'"**
   - Solution: Install umqtt library as shown in step 2

2. **WiFi connection fails**
   - Check 2.4GHz network (Pico 2 W doesn't support 5GHz)
   - Verify credentials in config.py
   - Check signal strength

3. **MQTT connection fails**
   - Verify AWS IoT endpoint URL
   - Check certificates and policies
   - Test with AWS IoT Test client

4. **Serial communication issues**
   - Verify wiring with multimeter
   - Check baudrate matches track controller
   - Test with oscilloscope if available

5. **Memory errors**
   - Reduce queue sizes in code
   - Enable garbage collection more frequently
   - Monitor with `gc.mem_free()`

### Debug Mode

Enable detailed logging:
```python
# In config.py
LOG_LEVEL = LOG_DEBUG
```

### Hardware Debugging

Use LED indicators for status:
```python
from machine import Pin
led = Pin(25, Pin.OUT)  # Built-in LED

# Blink patterns for different states
# Fast blink: Connecting to WiFi
# Slow blink: Connected, running normally
# Solid on: Error state
```

## Performance Optimization

### Memory Management
```python
# Monitor memory usage
import gc
gc.collect()  # Force garbage collection
print("Free:", gc.mem_free())
```

### Queue Tuning
Adjust queue sizes in respective modules based on your needs:
- Increase for high-traffic scenarios
- Decrease for memory-constrained situations

### Timing Optimization
Adjust refresh rates in `config.py`:
```python
MQTT_REFRESH_RATE_MS = 100      # MQTT publishing rate
SERIAL_REFRESH_RATE_MS = 100    # Serial communication rate
ANALYTICS_REFRESH_RATE_MS = 1000 # Analytics publishing rate
```

## Maintenance

### Regular Tasks
1. Monitor memory usage
2. Check WiFi connection stability
3. Verify MQTT message delivery
4. Update MicroPython firmware periodically

### Backup Configuration
Keep backup copies of:
- `config.py` with your settings
- AWS IoT certificates
- Wiring diagrams/photos

This completes the setup guide. Your Pico 2 W should now be ready to control the slot car race track!