import codecs
import io
import os
import sys

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

reload(sys)
sys.setdefaultencoding('utf-8')

# Variables
key_path = "key_path"
audio_folder = "audio_folder"
output_file = "output_file"


# Instantiates a client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
client = speech.SpeechClient()


def append_to_file(filename, string):
    with codecs.open(filename, 'a', "utf-8") as temp_file:
        temp_file.write(string + "\n")
        temp_file.close()


for flac_file in os.listdir(audio_folder):
    if flac_file.endswith(".flac"):
        file_name = os.path.join(audio_folder, flac_file)

        # Loads the audio into memory
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=44100,
            language_code='es-CL')

        # Detects speech in the audio file
        response = client.recognize(config, audio)

        for result in response.results:
            append_to_file(output_file, result.alternatives[0].transcript)
        print file_name + ' done!'
