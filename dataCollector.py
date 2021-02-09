import requests
import json
import os
from ratelimiter import RateLimiter

clan_id = 1000067803
ignoreSavedData = False	#currently unused. may impliment if i add ability to resume.
masterData = {}
shipsData = {}
shipsPath = 'ships.json'
dataPath = 'data.json'

ClanMemberIDsURL = f'https://api.worldofwarships.com/wows/clans/info/?application_id=2d227af62868c0359d39302df73da4ce&fields=name%2Cmembers_ids&clan_id={clan_id}'

def importShips():
	global shipsData
	if os.stat(shipsPath).st_size == 0:	#if file is empty, initialize the dict
		print('ships.json is empty.')
		shipsData = {'4289640432' : {'name' : 'Omaha', 'tier' : 5, 'type' : 'Cruiser'}}	#initialize json with *something*
	else:			#otherwise, import existing json
		with open(shipsPath) as json_file:
			shipsData = json.load(json_file)
	print(f'Exising ships imported from {shipsPath}')

def isShipInPool(ship_id):
	global shipsData
	try:
		temp = shipsData[str(ship_id)]
		return True
	except KeyError:
		return False

@RateLimiter(max_calls=10, period=1)
def GETShipData(ship_id):
	global shipsData
	shipLookupURL = f'https://api.worldofwarships.com/wows/encyclopedia/ships/?application_id=2d227af62868c0359d39302df73da4ce&fields=name%2Ctier%2Ctype&ship_id={ship_id}'
	shipLookupGET = requests.get(url = shipLookupURL)
	shipLookup = shipLookupGET.json()['data']
	try:
		if(shipLookup[str(ship_id)] == {}): return False
		shipsData[str(ship_id)] = {}
		shipsData[str(ship_id)]['name'] = shipLookup[str(ship_id)]['name']
		shipsData[str(ship_id)]['tier'] = shipLookup[str(ship_id)]['tier']
		shipsData[str(ship_id)]['type'] = shipLookup[str(ship_id)]['type']
		return True
	except:
		return False
	


def main():
	global masterData

	clanMemberIDsGET = requests.get(url = ClanMemberIDsURL)

	clanMemberIDs = clanMemberIDsGET.json()['data'][str(clan_id)]

	masterData = {'Clan Name' : clanMemberIDs['name']}

	masterData['Members'] = {}

	for UUID in clanMemberIDs['members_ids']:
		masterData['Members'][str(UUID)] = {}

	for UUID in masterData['Members']:
		print(f'Collecting ships for user <{UUID}>')
		shipsMemberOwnsGET = requests.get(url = f'https://api.worldofwarships.com/wows/ships/stats/?application_id=2d227af62868c0359d39302df73da4ce&account_id={UUID}&fields=ship_id&in_garage=1')
		try:
			shipsMemberOwns = shipsMemberOwnsGET.json()['data'][str(UUID)]
		except:
			continue

		for SID in shipsMemberOwns:
			tempSID = SID['ship_id']
			#potential problem spot. check method returns
			if isShipInPool(tempSID) or GETShipData(tempSID):
				#print(shipsData)
				masterData['Members'][UUID][str(tempSID)] = shipsData[str(tempSID)]
		saveMasterData()
		saveShipsData()
			
			
			

	print(masterData)

def saveShipsData():
	with open(shipsPath, 'w') as outfile:
		json.dump(shipsData, outfile)

def saveMasterData():
	with open(dataPath, 'w') as outfile:
		json.dump(masterData, outfile)



importShips();
main();
saveMasterData()
saveShipsData()
