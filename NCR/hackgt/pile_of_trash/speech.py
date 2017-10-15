import requests
import json

url = 'https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1?language=en-US&format=simple'
url_luis = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/47b3c748-a8e4-47f1-b32a-9f461d755c66"

files = {'file': open('test.wav', 'rb')}

headers = {
	"Accept": "application/json;text/xml",
	"Transfer-Encoding": "chunked",
	"Ocp-Apim-Subscription-Key": "1fc2f357e1da4b0d8670df97ba5f8aa6",
	"Content-Type": "audio/wav; codec=audio/pcm; samplerate=16000",
	"Host": "speech.platform.bing.com",
	"Transfer-Encoding": "chunked",
	"Expect": "100-continue"
}

r = requests.post(url, headers=headers)

print r.text


'''
r = json.loads(r.text)
if (r['RecognitionStatus'] == "Success"):
	query = r['NBest'][0]['Lexical']

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

else:
	print "Failed to translate voice!"
'''
