# NeMoASR

> Automatic speech recognition with speaker diarisation.

Based on:
- NVIDIA NeMo [Parakeet TDT 0.6b V3: Multilingual Speech-to-Text Model](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) for automatic speech recognition
- NVIDIA NeMo [Sortformer Diarizer 4spk v1](https://huggingface.co/nvidia/diar_sortformer_4spk-v1) for speaker diarisation


## Requirements
[Python 3.12+](https://www.anaconda.com/download/success)

## Setup
**Linux:**
```bash
sudo apt install ffmpeg
```
```bash
pip install git+https://github.com/HanBnrd/NeMoASR.git

```

**MacOS:**
```bash
brew install ffmpeg
```
```bash
pip install git+https://github.com/HanBnrd/NeMoASR.git
```

## Usage
```bash
nemoasr myfile.mp3
```


> ## Update NeMoASR
> ```bash
> pip install --upgrade git+https://github.com/HanBnrd/NeMoASR.git
> ```
>
