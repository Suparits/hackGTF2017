#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import httplib
import uuid
import json
import pyaudio
import wave

url_luis = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/47b3c748-a8e4-47f1-b32a-9f461d755c66"

def main():
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "./file.wav"


    ms_asr = Microsoft_ASR()
    ms_asr.get_speech_token()

    # start Recording
    audio = pyaudio.PyAudio()
    # stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print "Recording..."
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print "Finished recording."

    # print "recording..."
    # frames = []
    # while True:
    #     if stream.is_stopped():
    #         stream.start_stream()
    #         for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #             data = stream.read(CHUNK)
    #             frames.append(data)
    #     buf = stream.read(1024)
    #     if buf:
    #         stream.stop_stream()
    #         print "finished recording"


    # stop Recording
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    text, confidence = ms_asr.transcribe('./file.wav')
    
    query = text.strip()
    print "Text: " + query
    #print "Confidence: ", confidence
    
	payload = {
		'subscription-key': 'da37bd3f01e24ac091f0a982f33dbd5e',
		'verbose': 'true',
		'timezoneOffset': '-300',
		'spellCheck': 'true',
		'q':query
	}

	r = requests.post(url=url_luis, params=payload, headers=headers_luis)
	print r.text
	#r = json.loads(requests.post(url=url_luis, files=files, headers=headers_luis).text)

class Microsoft_ASR():
    def __init__(self):
        self.sub_key = '1fc2f357e1da4b0d8670df97ba5f8aa6'
        self.token = None
        pass

    def get_speech_token(self):
        FetchTokenURI = "/sts/v1.0/issueToken"
        header = {'Ocp-Apim-Subscription-Key': self.sub_key}
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        body = ""
        conn.request("POST", FetchTokenURI, body, header)
        response = conn.getresponse()
        str_data = response.read()
        conn.close()
        self.token = str_data
        #print "Got Token: ", self.token
        return True

    def transcribe(self, speech_file):

        # Grab the token if we need it
        if self.token is None:
            #print "No Token... Getting one"
            self.get_speech_token()

        endpoint = 'https://speech.platform.bing.com/recognize'
        request_id = uuid.uuid4()
        # Params form Microsoft Example
        params = {'scenarios': 'ulm',
                  'appid': 'D4D52672-91D7-4C74-8AD8-42B1D98141A5',
                  'locale': 'en-US',
                  'version': '3.0',
                  'format': 'json',
                  'instanceid': '565D69FF-E928-4B7E-87DA-9A750B96D9E3',
                  'requestid': uuid.uuid4(),
                  'device.os': 'linux'}
        content_type = "audio/wav; codec=""audio/pcm""; samplerate=16000"

        def stream_audio_file(speech_file, chunk_size=1024):
            with open(speech_file, 'rb') as f:
                while 1:
                    data = f.read(1024)
                    if not data:
                        break
                    yield data

        headers = {'Authorization': 'Bearer ' + self.token,
                   'Content-Type': content_type}
        resp = requests.post(endpoint,
                            params=params,
                            data=stream_audio_file(speech_file),
                            headers=headers)
        val = json.loads(resp.text)
        return val["results"][0]["name"], val["results"][0]["confidence"]

if __name__ == "__main__":
    main()