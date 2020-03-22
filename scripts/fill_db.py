# {'type': 'node', 'id': 16257496, 'lat': 49.5502832, 'lon': 8.6543267, 'tags': {'name': 'Lidl', 'shop': 'supermarket'}}

import json
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'data')

import requests

url = "https://controlservice.sicher-einkaufen.info/markt"

path = './marketsfiltered.json'


def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1
	
def custom_concat(strone, sthelse):
	if sthelse == None:
		strone += "null"
		return strone
	strone += "\""
	strone += str(sthelse)
	strone += "\""
	return strone

def main():

	data_file = open(path, 'r')
	temp = ""
	out = ""
	headers = {"Content-Type": "application/json; charset=utf-8"}
	length = file_len(path)
	
	print(length)
	for x in range(length):
		str  = data_file.readline()
		data = json.loads(str)
		print(x)
		out = ""
		temp += data["name"]
		out += "{\n\t\"Name\":\""
		out = custom_concat(out, data["name"])	
		out += "\",\n\t\"Company\":"
		out = custom_concat(out, data["company"])	
		out += ",\n\t\"GPSLocation\": {\n\t\t\"Lat\":"
		out = custom_concat(out, data["latitude"])
		out += ",\n\t\t\"Long\": "
		out = custom_concat(out, data["longitude"])
		out += "\n\t},\n\t\"Adresse\":\""
		out = custom_concat(out, data["address"])
		out += "\",\n\t\"Enabled\": true,\n\t\"Status\": null\n}"
		payload = out
		try:
			response = requests.request("POST", url, headers=headers, data = payload.encode('utf-8'))
		except:
			print("Error while posting data to server")

	data_file.close()
	print(out[0:1000])
 
if __name__ == '__main__':
	main()
	