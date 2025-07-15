import argparse
import logging
import os

from nemo.collections.asr.models import ASRModel, SortformerEncLabelModel
from pydub import AudioSegment

logging.disable(logging.CRITICAL)

SEGMENT_DURATION = 7  # max duration fitting in GPU (in mins)

argparser = argparse.ArgumentParser()
argparser.add_argument("file", type=str, help='mp3 file to transcribe')
args = argparser.parse_args()


def convert(mp3file):
    sound = AudioSegment.from_file(mp3file)
    sound = sound.set_channels(1)
    sound = sound.set_frame_rate(16000)
    filename = f"{os.path.splitext(mp3file)[0]}.wav"

    start = 0
    segment_number = 0
    wavfile_list = []
    segment_duration_ms = SEGMENT_DURATION * 60 * 1000  # mins to ms
    overlap_duration_ms = 5 * 1000  # 5 sec in ms

    while start < len(sound):
        end = min(start + segment_duration_ms, len(sound))
        segment = sound[start:end]
        wavfile = f"{filename}_part_{segment_number}.wav"
        wavfile_list.append(wavfile)
        segment.export(wavfile, format="wav")
        segment_number += 1
        start += segment_duration_ms - overlap_duration_ms

    return wavfile_list


def transcribe(wavfile):
    print(f"===\nTranscribing {wavfile}\n---")
    asr_model = ASRModel.from_pretrained(
        "nvidia/parakeet-tdt-0.6b-v2"
    )
    transcribed = asr_model.transcribe([wavfile], timestamps=True)
    transcribed = transcribed[0].timestamp['segment']
    del asr_model

    diar_model = SortformerEncLabelModel.from_pretrained(
        "nvidia/diar_sortformer_4spk-v1"
    )
    diarized = diar_model.diarize(audio=wavfile, batch_size=1)
    diarized = diarized[0]
    del diar_model

    with open(f"{os.path.splitext(wavfile)[0]}.txt", 'w') as fw:
        parsed_diarized = []
        for diar in diarized:
            start, end, speaker = diar.split()
            parsed_diarized.append([float(start), float(end), speaker])
        for tr in transcribed:
            start, text = tr['start'], tr['segment']
            speaker = None
            for diar in parsed_diarized:
                if round(diar[0]) <= round(start) <= round(diar[1]):
                    speaker = diar[-1]
                    break
            fw.write(f"{speaker}: {text}\n")


if __name__ == "__main__":
    wavfile_list = convert(args.file)
    for wavfile in wavfile_list:
        transcribe(wavfile)
