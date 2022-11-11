import React, { useEffect, useRef } from "react";
import { useViewer } from "react-kinesis-webrtc";
import { Loader } from "@aws-amplify/ui-react";


export default function WebRTCViewer({configProps}) {
    // const { accessKeyId, secretAccessKey, sessionToken } = async () => await Auth.currentCredentials();
    const videoRef = useRef();
    
    const {
        error,
        peer: { media } = {},
    } = useViewer(configProps);
    
    // Assign the peer media stream to a video source
    useEffect(() => {        
        if (videoRef.current) {
            videoRef.current.srcObject = media;
        }
    }, [media, videoRef]);
    
    // Display an error
    if (error) {
        return <p>An error occurred: {error.message}</p>;
    }

    if (!(media && media.active)) {
        return <Loader 
        size="large"
        variation="linear"
        filledColor="orange"
        paddingTop={150}
        maxWidth={300}
       />;
    }
    
    // Display the peer media stream
    return <video text-align={"center"} autoPlay ref={videoRef} />;
}
