import argparse
import logging
import os

from nemo.collections.asr.models import ASRModel, SortformerEncLabelModel
from pydub import AudioSegment


def convert(mp3file, segment_duration):
    sound = AudioSegment.from_file(mp3file)
    sound = sound.set_channels(1)
    sound = sound.set_frame_rate(16000)
    filename = f"{os.path.splitext(mp3file)[0]}"

    start = 0
    segment_number = 1
    wavfile_list = []
    segment_duration_ms = round(segment_duration * 60 * 1000)  # mins to ms
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


def main():
    logging.disable(logging.CRITICAL)
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file", type=str,
                           help='mp3 file to transcribe')
    argparser.add_argument("--max-duration", type=float, default=7,
                           help='max duration fitting on GPU in minutes')
    args = argparser.parse_args()
    wavfile_list = convert(args.file, args.max_duration)
    for wavfile in wavfile_list:
        transcribe(wavfile)


if __name__ == "__main__":
    main()
