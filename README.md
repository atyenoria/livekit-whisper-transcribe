# Description
This is the sample implementation of the asr websocket python server by using WebRTC livekit Egress. You can transcribe the speech audio file from livekit published audio track microphone per 30 seconds while saving the original audio file and resampled audio file that will be fed into faster_whisper. 

# Demo Video
https://www.loom.com/share/6452d9ca18f0473d9ee06e992083e161 


docker run --rm -e EGRESS_CONFIG_FILE=/out/config.yml --net=host -v ~/egress-test:/out livekit/egress


livekit-cli start-track-egress --api-key your-livekit-api-key --api-secret your-livekit-secret-key --request request.json


# livekit-whisper-transcribe

# the issues that I faced while debugging 
- 

# Author 
Akinori Nakajima
