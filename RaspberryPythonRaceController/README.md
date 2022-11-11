# Python Racer Helper
This project uses a RaspberryPi to control an internal race state and control communication with the slot car race track and the AWS Cloud for race stats.


## Iot Core Certificates
By default, we use IoT Core to talk to our RaspberryPi using MQTT. In order to get this to work, you need to create a "Thing" in IoT Core and generate certificates.
Follow this guide to do this: [https://docs.aws.amazon.com/iot/latest/developerguide/iot-moisture-create-thing.html](https://docs.aws.amazon.com/iot/latest/developerguide/iot-moisture-create-thing.html)

Then, Add the `AmazonRootCA1.pem`, `aws_cert.pem.crt` and `private.pem.key` to the `utils/certificate` folder of the project.

## Instructions - LOCAL LAPTOP
1. Clone the repository
2. `cd` into the repository
3. Create a virtual environment `python3 venv .venv`
4. `source .venv/bin/activate`
5. `pip install -r requirements.txt`
6. run tests: `python3 -m unittest tests.test_racer_helper`
7. run mqtt to Slot cars: `python3 main.py`
8. start debugger ui: `python3 byte_debugger.py`
9. `utils/constants.py` file will contain all settings that you need to adjust.
10. Make sure Mosquitto is installed if you want to run it locally
11. Run `<path_to_mosquitto> -c <path_to_mosquitto.conf>` in your terminal
12. E.g. `/usr/local/sbin/mosquitto -c /Documents/racer-helper-python/utils/mosquitto/mosquitto.conf`

## Instructions - Raspberry Pi
Steps:
1. Ensure you can access the source files of the 'RaspberryPythonRaceController' folder. You can upload the files via USB, or if you want to do it remotely, an option is to upload it to S3 using SSM:
2. Ensure the SSM agent is installed on RAPI and connected to your AWS account
3. Log in to SSM using the Fleet Manager service by starting a new remote terminal session.
4. `sudo su - [pi/<username of pi>]` in the terminal
5. Create an S3 bucket with a unique name in the AWS console, e.g. 'rapi-deployment-bucket'
6. Upload a Zipped version of the 'RaspberryPythonRaceController' folder, e.g. call it 'racer-helper.zip'.
7. Ensure AWS cli is installed on your RaspberryPi (`aws --version`), install it if it isn't.
8. Use AWS credentials (ideally temporary credentials), copy them in the SSM terminal
9. `cd Desktop`
10. `mkdir racer-helper-python`
11. `cd racer-helper-python`
12. `aws s3 cp s3://rapi-deployment-bucket/racer-helper.zip racer-helper.zip`
13. `unzip racer-helper.zip`

RUNNING THE RACE_HELPER:
1. `python --version` to ensure it’s 3.8+
2. `python -m venv .venv`
3. `source .venv/bin/activate`
4. `pip install --upgrade pip`
5. `pip install -r requirements.txt`
6. Adjust any values in utils/constants.py file
7. `python main.py` to run the helper broker

Running the Mosquitto Broker on the RaspberryPi (optional):
1. `sudo apt install -y mosquitto mosquitto-clients`
2. Adjust any values if necessary: `vim utils/mosquitto/mosquitto.conf`
3. sudo cp utils/mosquitto/mosquitto.conf /etc/mosquitto/mosquitto.conf
4. `sudo systemctl enable mosquitto.service`
5. If necessary, restart by using: `sudo systemctl restart mosquitto.service`

OPTIONAL: If you want to run the byte debugger GUI (not recommended on RAPI, do it on your laptop)
1. `pip install -r requirements-gui.txt`
2. If you get setup tools error `pip install --upgrade setuptools`
3. If you get attrdict error: `pip install attrdict`
4. If you get GTK+ error: `sudo apt-get install libgtk-3-dev libpulse-dev`