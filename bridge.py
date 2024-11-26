from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
from web3.middleware import geth_poa_middleware #Necessary for POA chains
import json
import sys
from pathlib import Path

source_chain = 'avax'
destination_chain = 'bsc'
contract_info = "contract_info.json"

warden_address = '0xE1291a15914B145b1b8e4d14262de323FeF41Cc8'
private_key = '418065defaaa52b069f5e37c3e20ec43670b0dd568e5beb472fbc8053260b270'

def connectTo(chain):
    if chain == 'avax':
        api_url = f"https://api.avax-test.network/ext/bc/C/rpc" #AVAX C-chain testnet

    if chain == 'bsc':
        api_url = f"https://data-seed-prebsc-1-s1.binance.org:8545/" #BSC testnet

    if chain in ['avax','bsc']:
        w3 = Web3(Web3.HTTPProvider(api_url))
        # inject the poa compatibility middleware to the innermost layer
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def getContractInfo(chain):
    """
        Load the contract_info file into a dictinary
        This function is used by the autograder and will likely be useful to you
    """
    p = Path(__file__).with_name(contract_info)
    try:
        with p.open('r')  as f:
            contracts = json.load(f)
    except Exception as e:
        print( "Failed to read contract info" )
        print( "Please contact your instructor" )
        print( e )
        sys.exit(1)

    return contracts[chain]



def scanBlocks(chain):
    """
        chain - (string) should be either "source" or "destination"
        Scan the last 5 blocks of the source and destination chains
        Look for 'Deposit' events on the source chain and 'Unwrap' events on the destination chain
        When Deposit events are found on the source chain, call the 'wrap' function the destination chain
        When Unwrap events are found on the destination chain, call the 'withdraw' function on the source chain
    """

    if chain not in ['source','destination']:
        print( f"Invalid chain: {chain}" )
        return
    
        #YOUR CODE HERE
    if chain == 'source':
        w3 = connectTo(source_chain)
    else:
        w3 = connectTo(destination_chain)

    info = getContractInfo(chain)
    address = info['address']
    abi = info['abi']
    contract = w3.eth.contract(address=address, abi=abi)

    current_block = w3.eth.block_number
    start_block = max(current_block - 5, 0)
    end_block = current_block

    if chain == 'source':
        event_filter = contract.events.Deposit.create_filter(fromBlock=start_block, toBlock=end_block)
        events = event_filter.get_all_entries()

        for event in events:
            token = event.args.token
            recipient = event.args.recipient
            amount = event.args.amount
            tx_hash = event.transactionHash.hex()

            des_w3 = connectTo(destination_chain)
            des_info = getContractInfo('destination')
            des_add, des_abi = des_info['address'], des_info['abi']

            des_contract = des_w3.eth.contract(address=des_add, abi=des_abi)

            nonce = des_w3.eth.get_transaction_count(warden_address)
            txn = des_contract.functions.wrap(token, recipient, amount).build_transaction({
                'chainId': 97,  # BSC testnet
                'gas': 100000,
                'gasPrice': des_w3.eth.gas_price,
                'nonce': nonce,
            })

            signed_txn = des_w3.eth.account.sign_transaction(txn, private_key=private_key)
            tx_hash = des_w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    else:
        event_filter = contract.events.Unwrap.create_filter(fromBlock=start_block, toBlock=end_block)
        events = event_filter.get_all_entries()

        for event in events:
            token = event.args.underlying_token
            recipient = event.args.to
            amount = event.args.amount
            tx_hash = event.transactionHash.hex()

            sou_w3 = connectTo(source_chain)
            sou_info = getContractInfo('source')
            sou_add, sou_abi = sou_info['address'], sou_info['abi']

            sou_contract = sou_w3.eth.contract(address=sou_add, abi=sou_abi)

            nonce = sou_w3.eth.get_transaction_count(warden_address)
            txn = sou_contract.functions.withdraw(token, recipient, amount).build_transaction({
                'chainId': 43113,  # AVAX testnet
                'gas': 100000,
                'gasPrice': sou_w3.eth.gas_price,
                'nonce': nonce,
            })

            signed_txn = sou_w3.eth.account.sign_transaction(txn, private_key=private_key)
            tx_hash = sou_w3.eth.send_raw_transaction(signed_txn.rawTransaction)
















