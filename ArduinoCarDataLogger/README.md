----

[[_TOC_]]

----

# Car Data Logger Software Installation

*NOTE: These steps assume that you have completed the Car Data Logger installation as documented in the* `Hardware` *folder.  You will need:
- The Certificate file that was generated when you registered the device
- Your AWS IoT Endpoint
- WiFi SSID and Password*

1. Download the `nano_rp2040_iot` folder to your PC and move it to the Arduino sketches home folder.  On a Windows PC this will typically be in `C:\Users\<UID>\Documents\Arduino`.
2. Open the Arduino IDE and then open the nano_rp2040_iot.ino file.  you should see two tabs appear, one for the ino file itself and one for the arduino_secrets.h file.
3. Update the following items in your arduino_secrets.h file:
- SECRET_SIDD: The SIDD of your WiFi network
- SECRET_PASS: The Password for your WiFi network
- SECRET_BROKER: The AWS IoT Endpoint
- SECRET_CERTIFICATE: The *PUBLIC* certificate you got when you registered the device.  *Note: The secret key is stored on your Arduino in the secure element.*
4. Click on the Upload button in the Arduino IDE to compile and upload the sketch.  
