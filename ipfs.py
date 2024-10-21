import requests
import json

def pin_to_ipfs(data):
        assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
        #YOUR CODE HERE

        payload = json.dumps(data)

        #authenticate with the Pinata API and 
        api_keys_and_secret = {'API Key': '84b66ca04d948cc54795', 'API Secret':'45035279697aa2adf024d17ed801eaed2f6ec6d8b5b7084553b562676de966ea'}
        url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

        #set up headers for api call
        headers = {'Content-Type': 'application/json', "pinata_api_key": api_keys_and_secret["API Key"], "pinata_secret_api_key": api_keys_and_secret["API Secret"]}

        #Sends a POST request to the Pinata API to pin the JSON data to IPFS including the URL, headers, and payload, which contains the JSON data to be pinned.
        response = requests.request("POST", url, headers=headers, data=payload)
        cid = response.json()["IpfsHash"]

	    return cid

def get_from_ipfs(cid,content_type="json"):
        assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
        #YOUR CODE HERE	
        
        #Constructing the URL to Retrieve IPFS Data:
        url = 'https://gateway.pinata.cloud/ipfs/'+cid

        #Fetching Data from IPFS
        data = requests.get(url).json()

        assert isinstance(data, dict), f"get_from_ipfs should return a dict"

        return data
