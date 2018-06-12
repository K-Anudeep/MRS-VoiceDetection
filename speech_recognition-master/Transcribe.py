
#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for async
batch processing.
Example usage:
    python transcribe_async.py resources/audio.raw
    python transcribe_async.py gs://cloud-samples-tests/speech/vr.flac
"""

import argparse
import io

# [START def_transcribe_gcs]
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))
# [END def_transcribe_gcs]


if __name__ == '__main__':
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
  "type": "service_account",
  "project_id": "my-project-transcribe",
  "private_key_id": "b4666df2ecd7af367091dd27091f5a5f04febeda",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCvPOp6KRq+oIM5\nRGkDJg31qBEGpmppBKS5BUdZU0A+D/3DIzKw+1/uL8yXzw++LjMFtIyqOIoIaWjK\nr3i/ows4/RhfPLApAT3cgYIOryweLKRlFejVsadMnBpWjTvS0UVbS3z2S1owpsD9\n78IJyUDU2VL4s3gkaL8FB0yeufOsOA6rwbZV4d0j6rKZ/a/NFDR3d5b8z6uwHCGF\nksWn2iME1+RX9UxH8p2tbhX+4NRBXLgaPanGWQl/cAcdWvo4HBSIFz4wixDIMkVR\nTyeO/uVHU1w5p/l0AY09pvJy7GxJfHQnSNqA+a/uWT8HkXN1OO80Uw2OJTNfqWhj\no7U3/3cfAgMBAAECggEABJW2F3bL2auew04kO+OFqfpjt6YoUpG/MuK4eIB9GyKV\nTm21UybAiR18X4cYr651wfMfWwoaUm4E7TNPbXQj7wca2XhfrjL3c2AlZEz2Uokd\nzqdBbZXgUq4i4kYqXTGsfDRVaKbqt9XPvCpxtoqAGmbf4jHlNXlSxhw9ckmwiROY\noicH7wrAUracJ5wO7wrYjUhmBUKvU6XTZaSP8cvw/OESiVU7Rn9ruUAO9ht5cviS\n4Yzh5yFii3FS3PywQxPnlxrsgewSLmWNUwfjqB0LgjkFac7AUpPeBda2Uo4Pady7\nin0jWRlwtbiSsQrWeva6VVdOZxhWHp29VnKVKTqWAQKBgQDbroHaY5yYMZcKEd/x\nLdhtOHkY+o/pLJ222/JQMmK0xVEfAIgsHOI2wgyh1jCMpPKVNTO3888vkyinIu+0\n+W+pZQWeN5LYV7qe5W2FhkGd+IXyK9iwYyToMABnbG3wzTrrSRbixu9DonqOSY88\nQ0RnL0bza3LyCy8cSgIo4V5ioQKBgQDMNW+4zNfgmOfu3nq6LX/rdP+XcNMuQjoU\ni8XYcOev0VV9UX0oxL1CMOM2uNj0ohWnjeIDiZZXaR0HDGbnUfVG2weHwlbDBQLW\n6B3ydO1PYTyMRO05vQbB3MT56l5WeHOwZkFrctssUnJWH+uX3yl9D41VsjZ0DKK2\n+JkL9+lBvwKBgCaTOhITM8g1zQPjp6M+HabwJ7OPK/4R64/Uh3Q1pMeBboE3IrI8\nUCy1Xmp8pgHMZRx2PyKqGVONT7IpnFX3BviD2LyznYGHxilouBaeQJ9wqHSh5mby\nweRTqX5/t751C0eNigtAS3tg6Ixbtl8qoLRNxPOxhnmiJR+ej0qGaICBAoGACIpv\nmsYOfVlH0gjCD0lZ4UoqanYQjw28CiHya2QFfKf/sFcZKfxYgg0zY5WFlW22BCT9\n//HgNNWznhjZsPEPliARB4+MO2nZPY3Fut9DEZ/afW9gkJqkTrViE6XGvk0ZYZZV\nRB4wpoDoQUvieZ6eyJk+6weiGWZx478v/30l51cCgYEAytDJsbtcOPYpc2hD5g13\nYl3wBK0g7ypibnME87s5kQ0O8XfiMdEk//eqGTghSYE+QCqvW9erPUO/5owZDif/\nZgcf+YYXahD5KXY+K1o43QN112Rz7ojpDzXo0PwZQc6B7r78gALavlO3jrr7wone\nTdMRGhw+Ir1GAvzNHY9Rd4s=\n-----END PRIVATE KEY-----\n",
  "client_email": "transcribe@my-project-transcribe.iam.gserviceaccount.com",
  "client_id": "109362739639526830130",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/transcribe%40my-project-transcribe.iam.gserviceaccount.com"
}"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs(args.path)