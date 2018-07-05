# InternProject2018
June 2018 Intern Project on Audio file transcription

Transcribing audio files into text and creating a dataset off of it to ultimately use it for a Movie Recommending System or in short MRS™.

This process uses Google's Cloud Speech API. Local file transcriptions are limited to 60s audio clips which takes up time for bulk transcriptions which is why we use Google Cloud Storage(GCS) to transcribe since it has a 80min limit on transcription which is more than enough for this project.

Upload the files of supported audio formats/encoding to GCS and run the file location through the script for the result.

Supported audio files: 16bit, 16khz, mono FLAC files are the choosen format as they take low space compared to WAV files. All the audio conversions are currently done through Audacity.


WORK IN PROGRESS
