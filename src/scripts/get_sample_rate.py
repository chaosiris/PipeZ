import ffmpeg
import sys

def get_audio_sample_rate(file_path):
    probe = ffmpeg.probe(file_path)
    audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
    if audio_stream is None:
        raise Exception('No audio stream found')
    return int(audio_stream['sample_rate'])

if __name__ == "__main__":
    file_path = sys.argv[1]
    sample_rate = get_audio_sample_rate(file_path)
    print(sample_rate)