import requests
import json

PINATA_API_KEY = "84b66ca04d948cc54795"
PINATA_SECRET_API_KEY = "45035279697aa2adf024d17ed801eaed2f6ec6d8b5b7084553b562676de966ea"
PINATA_API_URL = "https://api.pinata.cloud"

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	assert isinstance(data, dict), f"Error: pin_to_ipfs expects a dictionary"

    json_data = json.dumps(data)

    headers = {
        'pinata_api_key': PINATA_API_KEY,
        'pinata_secret_api_key': PINATA_SECRET_API_KEY
    }

    payload = {
        'pinataContent': data,
    }

    response = requests.post(f"{PINATA_API_URL}/Pinning/pinJSONToIPFS", headers=headers, json=payload)
    
    if response.status_code == 200:
        res_json = response.json()
        cid = res_json['IpfsHash']
        return cid
    else:
        raise Exception(f"Error pinning to IPFS: {response.content}")
	#return cid

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	#YOUR CODE HERE	
	response = requests.get(f"https://gateway.pinata.cloud/ipfs/{cid}")

	if response.status_code == 200:
        json_data = response.text
        
        if content_type == "json":
            data = json.loads(json_data)
            assert isinstance(data, dict), f"Error: get_from_ipfs should return a dict"
            return data
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
    else:
        raise Exception(f"Error getting data from IPFS: {response.content}")

	#assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	#return data
