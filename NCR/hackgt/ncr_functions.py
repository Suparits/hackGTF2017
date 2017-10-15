import sys
import requests
import json
from os import system

url = "https://hackgt-api.ncrcloud.com"
url_price = "/catalog/item-prices/get-multiple/"
url_search = "/catalog/items?sortDirection=ASC&longDescriptionPattern="
url_suggest = "/catalog/items/suggestions?descriptionPattern="

headers = {
    'accept': "application/json",
	'authorization': "Basic L29yZy0xL2FkbWluOkNoYW5nM20zISEtYWRtaW4tb3JnLTE=",
    'content-type': "application/json",
    'nep-enterprise-unit': "eafe5b77b5594e9ab575ed4b41d6ee37",
    'nep-organization': "org-1",
	'nep-application-key': "8a82859f5ef21870015ef2fa5e5f0000"
}

def suggest(query):
	pUrl = url + url_suggest + query 
	print "Query: " + pUrl
	r = requests.get(url=pUrl, headers=headers)
	print r.text

def searchItem(query):
	pUrl = url + url_search + '*' + query + '*'
	#print "Query: " + pUrl
	r = requests.get(url=pUrl, headers=headers)
	r = json.loads(r.text)

	itemCode = r['pageContent'][0]['itemId']['itemCode']
	itemName = r['pageContent'][0]['shortDescription']['value']
	
	r = getPrice([itemCode,])
	itemPrice = r['itemPrices'][0]['price']
	dollars = int(itemPrice)
	cents = int((itemPrice-int(itemPrice))*100)

	sayThis = "The price of " + itemName + " is " + str(dollars) + " dollars"

	if (cents !=0):
		sayThis = sayThis + " and " + str(cents) + " cents."

	return sayThis



def getPrice(listOfIds):
	pUrl = url + url_price
	payload = {"itemIds": []}
	
	for item in listOfIds:
		payload["itemIds"].append({"itemCode": item})

	r = requests.post(url=pUrl, data=json.dumps(payload), headers=headers)
	#print r.text
	return json.loads(r.text)
	
def cheapestItem(query):
	pUrl = url + url_search + '*' + query + '*'
	#print "Query: " + pUrl

	
	r = requests.get(url=pUrl, headers=headers)
	print r.text
	r = json.loads(r.text)

	cheapestItem = ""
	cheapestPrice = 999999.99

	for obj in r['pageContent']:
		tmp = getPrice([obj['itemId']['itemCode']],)
		tmp = tmp['itemPrices'][0]['price']
		
		print "Cost: " + str(tmp)
		if tmp < cheapestPrice:
			cheapestPrice = tmp
			cheapestItem = obj['shortDescription']['value']


	dollars = int(cheapestPrice)
	cents = int((cheapestPrice-int(cheapestPrice))*100)

	sayThis = "The cheapest item is " + str(cheapestItem) + " which costs " + str(dollars) + " dollars"

	if (cents !=0):
		sayThis = sayThis + " and " + str(cents) + " cents."

	return sayThis

#searchItem("extra virgin olive oil")
#getPrice(["13a1d299-082c-4663-a067-1046a86851bb", "ceb9eb06-baee-445b-a501-b117696ecc40"])


def main():
	if (len(sys.argv) < 2):
		sys.stdout.write("[Error] No action passed!")
	else:
		if (sys.argv[1] == "Price"):
			sayThis = searchItem(sys.argv[2])
			system('say ' + sayThis)
		elif (sys.argv[1] == "Cheapest Price" and len(sys.argv) == 2):
			searchItem(sys.argv[2])
		else:
			print "Nothing else matched."
if __name__ == "__main__":
	main()
