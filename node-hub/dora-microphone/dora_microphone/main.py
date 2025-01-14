import os
import time as tm

import numpy as np
import pyarrow as pa
import sounddevice as sd
from dora import Node

MAX_DURATION = float(os.getenv("MAX_DURATION", "0.1"))
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "16000"))


def main():
    # Initialize buffer and recording flag
    buffer = []
    start_recording_time = tm.time()
    node = Node()

    always_none = node.next(timeout=0.001) is None
    finished = False

    # noqa
    def callback(indata, frames, time, status):
        nonlocal buffer, node, start_recording_time, finished

        if tm.time() - start_recording_time > MAX_DURATION:
            audio_data = np.array(buffer).ravel().astype(np.float32) / 32768.0
            node.send_output("audio", pa.array(audio_data))
            if not always_none:
                event = node.next(timeout=0.001)
                finished = event is None
            buffer = []
            start_recording_time = tm.time()
        else:
            buffer.extend(indata[:, 0])

    # Start recording
    with sd.InputStream(
        callback=callback, dtype=np.int16, channels=1, samplerate=SAMPLE_RATE
    ):
        while not finished:
            sd.sleep(int(1000))
