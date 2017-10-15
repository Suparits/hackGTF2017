import requests
import json

url_luis = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/47b3c748-a8e4-47f1-b32a-9f461d755c66"

headers_luis = {
	'Ocp-Apim-Subscription-Key': 'da37bd3f01e24ac091f0a982f33dbd5e'
}

payload = {
	'subscription-key': 'da37bd3f01e24ac091f0a982f33dbd5e',
	'verbose': 'true',
	'timezoneOffset': '0',
	'spellCheck': 'true',
    'verbose': 'false',
    'staging': 'false',
	'q': 'how much does milk cost'
}

r = requests.get(url=url_luis, params=payload, headers=headers_luis)
print r.text
