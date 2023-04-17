import asyncio
import logging
import time
from io import BytesIO
from aiohttp import web
from pydub import AudioSegment
from faster_whisper import WhisperModel
import wave

logging.basicConfig(level=logging.INFO)

model_size = "large-v2"
model = WhisperModel(model_size, device="cuda", compute_type="auto")

async def save_and_transcribe(audio_data):
    timestamp = time.strftime("%Y-%m-%dT%H-%M-%S", time.gmtime())
    original_file_name = f"original_{timestamp}.wav"
    with wave.open(original_file_name, "wb") as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(48000)
        wav_file.writeframes(audio_data)
    logging.info(f"Original audio file saved as {original_file_name}")

    audio = AudioSegment.from_raw(BytesIO(audio_data), sample_width=2, frame_rate=48000, channels=2)
    mono_audio = audio.set_channels(1)
    resampled_audio = mono_audio.set_frame_rate(16000)
    resampled_file_name = f"resampled_{timestamp}.wav"
    resampled_audio.export(resampled_file_name, format="wav")
    logging.info(f"Resampled audio file saved as {resampled_file_name}")

    segments, info = model.transcribe(resampled_file_name, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

async def audio_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    audio_data = bytearray()

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.BINARY:
                audio_data.extend(msg.data)

                if len(audio_data) >= 48000 * 2 * 2 * 30:
                    current_audio_data = audio_data.copy()
                    audio_data = bytearray()

                    asyncio.create_task(save_and_transcribe(current_audio_data))
            elif msg.type == web.WSMsgType.ERROR:
                logging.error(f"WebSocket closed with exception: {ws.exception()}")
    except Exception as e:
        logging.error(f"Error receiving audio data: {e}")

    return ws

app = web.Application()
app.router.add_route("GET", "/ws", audio_handler)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
