import codecs
import io
import os
import sys

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import storage

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


for flac_file in sorted(os.listdir(audio_folder)):
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

        try:
            response = client.recognize(config, audio)
        except:
            storage_client = storage.Client()

            bucket = 'bucket'
            bucket_file_name = flac_file

            gc_bucket = storage_client.get_bucket(bucket)
            blob = gc_bucket.blob(bucket_file_name)

            with open(file_name, 'rb') as audio_file:
                blob.upload_from_file(audio_file)

            audio = types.RecognitionAudio(uri='gs://' + bucket + '/' + bucket_file_name)

            operation = client.long_running_recognize(config, audio)
            response = operation.result(timeout=90)

        for result in response.results:
            append_to_file(output_file, result.alternatives[0].transcript)
        print file_name + ' done!'
