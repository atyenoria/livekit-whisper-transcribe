# Description
This is the sample implementation of the asr websocket python server by using WebRTC livekit Egress. You can transcribe the speech audio file from livekit published audio track microphone per 30 seconds while saving the original audio file and resampled audio file that will be fed into faster_whisper. 

# Demo Video
https://www.loom.com/share/6452d9ca18f0473d9ee06e992083e161 


docker run --rm -e EGRESS_CONFIG_FILE=/out/config.yaml --net=host -v ~/egress-test:/out livekit/egress

livekit-cli start-track-egress --api-key your-livekit-api-key --api-secret your-livekit-secret-key --request request.json

# Preparation 
livekit-server https://github.com/livekit 
egress https://github.com/livekit/egress
faster whisper https://github.com/guillaumekln/faster-whisper
AWS g5.xlarge instance
Vultr VPS for livekit 
ChatGPT4 for any unknown issues. 

# Setup  
0. run the egress by "docker run --rm -e EGRESS_CONFIG_FILE=/out/config.yaml --net=host -v ~/egress-test:/out livekit/egress" after setting config.yaml
1. Publish your audio track and check the audio track and room id from livekit console log
2. update the request.json accoring to the result
3. run "livekit-cli start-track-egress --api-key your-livekit-api-key --api-secret your-livekit-secret-key --request request.json" after starting "asr-server.py"
4. you can see the transcription from the terminal and check the original and resampled audio file to detect the audio issues 

# the issues that I faced while debugging 
- Head part audio cut off issue when receiving the websocket audio streaming from egress 
- Cuda error on g5.xlarge instance (sudo apt install nvidia-driver-470 worked)
- Resample from "pcm 16bit 48Khz 2channel" to "pcm 16bit 16Khz 1channel"
- 

# Author 
Akinori Nakajima
