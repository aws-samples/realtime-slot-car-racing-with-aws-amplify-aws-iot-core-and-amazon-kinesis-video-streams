# Live-streaming with Raspberry Pi and Kinesis Video Streams WebRTC.

## Overview

To create a live streaming experience, we will use Kinesis Video Streams WebRTC based signaling channel. It is specifically
designed with live streaming capacitiy for audio and video. We are going to divide our work into the following sections:
- stream producer - the source of the stream from which the live stream is originating. In our case it's the Rapi with the camera module.
- stream consumer - these are simply the viewers of the stream. In our case they'll be consuming the stream via a web browser,
  powered by AWS Amplify. The instruction setup is available in the `/RaceFrontend/README.md` file.

## Prerequisites:
- KVS signaling channel (has to be created manually as it's not available in all regions)
- Raspberry Pi model 4 (RAPI) with a camera module 2 or other HDMI to CSI adapter.
    - We highly recommend to configure SSM Agent on the Raspberry Pi. Follow the installation guide [here](https://docs.aws.amazon.com/systems-manager/latest/userguide/agent-install-deb.html)


## Setting up stream producer

These steps assume you have CLI connection to the raspberry pi and have validated that the camera connected to the Pi works.
Check out the steps on how to configure the RaPi camera [here](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/0)

1.  Open the terminal on the Raspberry Pi and execute
    ```bash
    git clone --recursive https://github.com/mehow-juras/amazon-kinesis-video-streams-webrtc-sdk-c
    mkdir -p amazon-kinesis-video-streams-webrtc-sdk-c/build; cd amazon-kinesis-video-streams-webrtc-sdk-c/build; cmake ..
    sudo apt-get install libssl-dev libcurl4-openssl-dev liblog4cplus-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-base-apps gstreamer1.0-plugins-bad gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-tools
    ```
2. Build the project by running ```make``` in the amazon-kinesis-video-streams-webrtc-sdk-c/build directory. Note: this command
   may take a while to execute. Give it time.
3. In the meantime you'll have some time to setup your permissions. You need to create an IAM user credentials to allow the Pi to send video stream to the KVS signaling channel. Navigate to the IAM console and create an user with the following policy:
    ```
    {
       "Version":"2012-10-17",
       "Statement":[
          {
              "Effect":"Allow",
              "Action":[
                "kinesisvideo:DescribeSignalingChannel",
                "kinesisvideo:CreateSignalingChannel",
                "kinesisvideo:GetSignalingChannelEndpoint",
                "kinesisvideo:GetIceServerConfig",
                "kinesisvideo:ConnectAsMaster",
              ],
              "Resource":"arn:aws:kinesisvideo:*:*:channel/{$CHANNEL_NAME}/*"
          }
       ]
    }
    ```
   Note: remember to replace the channel name with your own channel name. Also keep the access key and secret access key as it'll become handy in the next step.

4. Create a new file on rapi called `start_streaming.sh` using `vi` with the following contents:
    ```bash
    #!/bin/bash
    export AWS_ACCESS_KEY_ID=<your AWS account access key>
    export AWS_SECRET_ACCESS_KEY=<your AWS account secret key> 
    
    ./amazon-kinesis-video-streams-webrtc-sdk-c/build/samples kvsWebrtcClientMaster $YOUR_KVS_CHANNEL_NAME
    ```
5. Execute the script by running ```./start_streaming.sh``` You should see logging output from the script.
6. Now you can navigate to your KVS channel in your AWS console and view stream from your device there.

