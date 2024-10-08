import json

import pyaudio
import vosk

if __name__ == '__main__':
    model = vosk.Model(lang="en-us")
    rec = vosk.KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8192)
    print("Listening for speech. Say 'Terminate' to stop.")
    # Start streaming and recognize speech
    while True:
        data = stream.read(4096)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            recognized_text = result['text']
            # Write recognized text to the file
            print(recognized_text)
            # Check for the termination keyword
            if "terminate" in recognized_text.lower():
                print("Termination keyword detected. Stopping...")
                break
    stream.stop_stream()
    stream.close()
    p.terminate()