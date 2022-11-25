# Race frontend

This part of the project consists of a web application that allows you to:
- perform race management tasks of the track
- allow users to select and control a particular car on the track using their own browser
- show the dashboard with a live video stream and current race leaderboard. It is based on Kinesis Video Streams signaling channel
  using WebRTC protocol and a live stream produced by your own stream producer. (Setup instructions in `/StreamProducer` directory)


## Prerequisites:
* AWS account
* [Amplify CLI](https://docs.amplify.aws/cli/start/install/)
* [Node and NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
* An S3 bucket called "race-asset-bucket-$INSERT-RANDOM-NUMBER" in the same aws account as this project
* Create a Kinesis Video Streams Signalling channel in the region of your choosing. Ideally somewhere that's closest to your viewers.
  Check out the [instructions here](https://docs.aws.amazon.com/kinesisvideostreams-webrtc-dg/latest/devguide/gs-createchannel.html)

## Setup:

1. Run `npm install` in the `/RaceFrontend` directory.
2. Edit `amplify/backend/video/raceLiveStream/props.json` and
   `amplify/backend/video/raceLiveStream/build/raceLiveStream-livestream-workflow-template.json` and add your random number ($INSERT-RANDOM-NUMBER) to the S3 bucket name "race-asset-bucket"
3. Make sure you created your .env file. You can do so by copying the contents of `.env.example` file. Make sure you fill out environment details related to your Kinesis Video Streams channel
    ```javascript
    REACT_KVS_CHANNEL_REGION=<your_kvs_channel_region>
    REACT_KVS_CHANNEL_ARN=<your_channel_arn>
    ```
4. Run `amplify init` and fill out the prompts according to your needs.
    - _NOTE_: you might have to run `amplify configure` to setup your aws credentials first.
5. Run `amplify push` to deploy your project.
   _Note_: you need to add appropriate environment variables to the deployment pipeline in amplify or hardcode the details of your KVS channel in the UI.
6. Attach viewer IAM policy to the Cognito Auth Role.

   Navigate to the IAM service in your AWS console. Find the role created by Cognito for
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
          "Resource": {$YOUR_CHANNEL_ARN}
        }
      ]
    }    
    ```
7. Validate your deployment.

   You can do so by running your front-end locally with ```npm start``` and viewing your stream on `localhost:3000/race-overview`
   You should see the same video stream coming from your stream producer in your browser window.

   _Note_: make sure that the stream producer is still running if you cannot see the stream showing up on your browser. Also try refreshing the page.


## Next steps:
- deploy and host your website with Amplify so more users can play online: [steps available here](https://docs.aws.amazon.com/amplify/latest/userguide/getting-started.html)
