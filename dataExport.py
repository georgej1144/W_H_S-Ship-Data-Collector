import json
import requests

tier = 8;
outputKey = "AirCarrier"

outputString = ""
shipsChecked = []

allData = {}

allShips = {}

with open('data.json') as json_file:
	allData = json.load(json_file)

with open('ships.json') as json_file:
	allShips = json.load(json_file)

allShipsSorted = allShips
allShipsSorted = dict(sorted(allShipsSorted.items()))

allDataSorted = allData

for userID in allDataSorted['Members']:
	allDataSorted['Members'][str(userID)] = dict(sorted(allData['Members'][str(userID)].items()))

#cross reference and output


for userID in allDataSorted['Members']:

	nameFromIDURL = f'https://api.worldofwarships.com/wows/clans/accountinfo/?application_id=2d227af62868c0359d39302df73da4ce&account_id={userID}&fields=account_name'

	nameFromIDGET = requests.get(url = nameFromIDURL)

	nameFromID = nameFromIDGET.json()['data'][str(userID)]['account_name']

	outputString += nameFromID + '\t'

	for shipID in allShipsSorted:
		if allShipsSorted[shipID]['tier'] == tier and allShipsSorted[shipID]['type'] == outputKey:
				if allShipsSorted[shipID]['name'] not in shipsChecked:
					shipsChecked.append(allShipsSorted[shipID]['name'])
				if shipID in allDataSorted['Members'][str(userID)]:
					outputString += '1\t'
				else:
					outputString += '0\t'
	outputString = outputString[0:len(outputString)-1]
	outputString += '\n'

print(outputString)
print(shipsChecked)

text_file = open(f'output-{outputKey}-{tier}.txt', "w")


shipOutputString = " \t"

for index in range(len(shipsChecked)):
	shipOutputString += shipsChecked[index] + '\t'
shipOutputString = shipOutputString[0:len(shipOutputString)-1]
shipOutputString += '\n'

text_file.write(shipOutputString)
text_file.write(outputString)
text_file.close()
