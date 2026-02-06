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
conda create -n nemoasr python=3.12
conda activate nemoasr
pip install uv
uv pip install git+https://github.com/HanBnrd/NeMoASR.git
```

**MacOS:**
```bash
brew install ffmpeg
```
```bash
conda create -n nemoasr python=3.12
conda activate nemoasr
pip install uv
uv pip install git+https://github.com/HanBnrd/NeMoASR.git
```

## Usage
```bash
nemoasr myfile.mp3
```
> *Note: running this for the first time may be long as the models need to be downloaded.*

The default configuration is cutting long audio files into chunks of 7 mins which should work on machines with little VRAM or RAM. However, the chunk duration can be changed. For example if the VRAM or RAM capacity is bigger:
```bash
nemoasr myfile.m4a --max-duration=12
```
This will cut a long audio file in chunks of 12 mins maximum.

> ## Update NeMoASR
> ```bash
> pip install --upgrade git+https://github.com/HanBnrd/NeMoASR.git
> ```
>
