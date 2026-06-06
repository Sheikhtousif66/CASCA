import os
import json
import queue
import time
import audioop
import sounddevice as sd
from vosk import Model, KaldiRecognizer

MODEL_PATH=os.path.join(
    os.path.dirname(__file__),
    "vosk-model-small-en-us-0.15"
)

model=Model(MODEL_PATH)

q=queue.Queue()


def callback(indata,frames,time_info,status):
    if status:
        print(status)
    q.put(bytes(indata))


def listen():

    recognizer=KaldiRecognizer(model,16000)

    print("\n🎤 Listening... Speak now\n")

    start=time.time()
    volumes=[]

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback
    ):

        while True:

            data=q.get()

            rms=audioop.rms(data,2)
            volumes.append(min(rms/10000,1.0))

            if recognizer.AcceptWaveform(data):

                result=json.loads(
                    recognizer.Result()
                )

                text=result.get(
                    "text",""
                ).strip()

                if text:

                    duration=time.time()-start

                    avg_volume=(
                        sum(volumes)/len(volumes)
                        if volumes else 0
                    )

                    stats={
                        "volume":avg_volume,
                        "duration":duration
                    }

                    print(
                      f"You (voice): {text}"
                    )

                    return text,stats