# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## PREREQUISITES:
* [Amplify CLI](https://docs.amplify.aws/cli/start/install/)
* Java (JDK) for [mocking](https://docs.amplify.aws/cli/usage/mock/)
* [Node and NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
* An S3 bucket called "race-asset-bucket-$INSERT-RANDOM-NUMBER"



## SETUP:
* `npm install`
* Edit `amplify/backend/video/raceLiveStream/props.json` and `amplify/backend/video/raceLiveStream/build/raceLiveStream-livestream-workflow-template.json` and add your random number to the S3 bucket name "race-asset-bucket"
* `amplify init`
* `amplify push`
* To run locally:
  * Rename `.env.example` file to `.env` and adjust as appropriate
  * `amplify mock` in one terminal
  * `npm start` in another terminal


Local Mosquitto (MQTT) setup:
* Download and Mosquitto: [https://mosquitto.org/download/](https://mosquitto.org/download/)
* Configure the config file:
  * File: `/usr/local/etc/mosquitto/mosquitto.conf` on Mac
  * Add the following at the top and save:
  ```
  port 1883
  protocol mqtt

  listener 9001
  protocol websockets

  allow_anonymous true
  ```
* Run the broker, e.g. on Mac: `/usr/local/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf -v`

# Live streaming with Raspberry Pi and Kinesis Video Streams WebRTC.

## Prerequisites:
- KVS signaling channel (has to be created manually as it's not available in all regions)
- Raspberry Pi model 4 (RAPI) with a camera module 2 or other HDMI to CSI adapter.
  - We highly recommend to configure SSM Agent on the Raspberry Pi. Follow the installation guide [here](https://docs.aws.amazon.com/systems-manager/latest/userguide/agent-install-deb.html)

## Overview

To create a live streaming experience, we will use Kinesis Video Streams WebRTC based signaling channel. It is specifically
designed with live streaming capacitiy for audio and video. We are going to divide our work into the following sections:
- stream producer - the source of the stream from which the live stream is originating. In our case it's the Rapi with the camera module.
- stream consumer - these are simply the viewers of the stream. In our case they'll be consuming the stream via a web browser,
  powered by AWS Amplify.

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
3. In the meantime you'll have to setup an IAM user to help to allow the Pi to send video stream to the KVS signaling channel. Navigate to the IAM console and create an user with the following policy:
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
    export AWS_ACCESS_KEY_ID= <AWS account access key>
    export AWS_SECRET_ACCESS_KEY= <AWS account secret key> 
    
    ./amazon-kinesis-video-streams-webrtc-sdk-c/build/samples kvsWebrtcClientMaster {$YOUR_KVS_CHANNEL_NAME}
    ```
5. Execute the script by running ```./start_streaming.sh``` You should see logging output from the script.
6. Now you can navigate to your KVS channel in your AWS console and view stream from your device there.

# Setting up stream consumer

The stream consumer aka viewer is setup through the Amplify based web application. In this repository,
you can navigate to the /src/web-components/webrtc-viewer.jsx page and how it's embedded into a page in /src/pages/race-overview.jsx.

This part already assumes you have initialized and deployed the Amplify project.

## Setup steps

1. Navigate to the /src/pages/race-overview.jsx file. At the top of the file fill out the appropriate
   variables listed below with details corresponding to your project.
    ```javascript
    const KVSCHANNEL_REGION = <YOUR_KVS_CHANNEL_REGION>
    const KVSCHANNEL_ARN = <YOUR_KVS_CHANNEL_ARN> 
    ```

  2. Attach viewer IAM policy to the Cognito Auth Role. Navigate to the IAM service in your AWS console. Find the role created by Cognito for
     Authenticated users. Simply search for the phrase `AuthRole`. You should be looking for a role in the following format {project name}-{amplify env}-{app id}-authRole
     Once you found the role, attach the following policy to that IAM role:
   ```
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "kinesisvideo:ConnectAsViewer",
                   "kinesisvideo:DescribeSignalingChannel",
                   "kinesisvideo:GetIceServerConfig",
                   "kinesisvideo:GetSignalingChannelEndpoint"
               ],
               "Resource": {YOUR_CHANNEL_ARN}
           }
       ]
   }
   ```

3. Save the file and validate if the stream works. You can do so by either running your front-end locally with
   ```npm start``` and viewing your stream on localhost:3000 or run ```amplify push``` to validate your branch in the remote environment.
   You should see the same video stream on your browser as you have on the KVS signaling channel in your AWS console.

   Note: make sure that the stream producer is still running if you cannot see the stream showing up on your browser. Also try refreshing the page.
