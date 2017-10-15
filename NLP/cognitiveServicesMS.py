#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import httplib
import uuid
import json
import pyaudio
import wave
import luis
from AppKit import NSSpeechSynthesizer
import pyttsx
from os import system
#from string2Speech import speak


def main():
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "/Users/nrakoski/Documents/GitHub/NCR/NLP/file.wav"


    ms_asr = Microsoft_ASR()
    ms_asr.get_speech_token()

    # start Recording
    audio = pyaudio.PyAudio()
    # stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print "recording..."
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print "finished recording"

    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    text, confidence = ms_asr.transcribe(WAVE_OUTPUT_FILENAME)

    # text, confidence = ms_asr.transcribe('/Users/nrakoski/Documents/GitHub/NCR/NLP/sample.wav')
    # text, confidence = ms_asr.transcribe(stream)
    print "Text: ", text
    print "Confidence: ", confidence

    # l = luis.Luis(url='https://l.facebook.com/l.php?u=https%3A%2F%2Fwestus.api.cognitive.microsoft.com%2Fluis%2Fv2.0%2'
    #                   'Fapps%2F47b3c748-a8e4-47f1-b32a-9f461d755c66%3Fsubscription-key%3Dda37bd3f01e24ac091f0a982f33db'
    #                   'd5e%26timezoneOffset%3D-480%26verbose%3Dtrue%26spellCheck%3Dtrue%26q%3D&h=ATM-5kTUv1f7UjIpjzUHw'
    #                   'x6SGn78I833Nz4tAwWOKK7S7yQz-0cJQFGwv4ADhDjtz93-pr15RzT1Vi8pkxWUZUB0hMPi1zDW_ms8vonpyQyRbQXC780T'
    #                   'ubEkRc1FAIXlONW44yluHoJQxwSpK1o')
    # # Send text to be analyzed:
    # r = l.analyze(text)
    # print r.intents
    #
    # # See all identified entities:
    # print r.entities
    #
    # best = r.best_intent()
    # print best
    # print best.intent
    # print best.score

    # Speach to Text
    # engine = pyttsx.init()
    # engine.say(text)
    # engine.runAndWait()
    system('say ' + text)

    return




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
        print "Got Token: ", self.token
        return True

    def transcribe(self, speech_file):

        # Grab the token if we need it
        if self.token is None:
            print "No Token... Getting one"
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
    main(input1, input2)
