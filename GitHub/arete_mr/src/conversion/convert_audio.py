from pydub import AudioSegment
import os

def convert_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="wav")

if __name__ == '__main__':
    input_file = 'data/uploads/input_audio.mp3'
    output_file = 'data/uploads/output_audio.wav'
    convert_to_wav(input_file, output_file)
    print(f'Converted {input_file} to {output_file}')
