import web3
import requests
import time

bsc = 'https://bsc.getblock.io/mainnet/?api_key=49f921ce-971b-4fcc-acc9-bedc55da95d9'
# address = '0xb9abf98cab2c8bd2adf8282e52bf659adb0260fe'
address = '0x7ee058420e5937496F5a2096f04caA7721cF70cc'

w3 = web3.Web3(web3.HTTPProvider(bsc))

url_eth = 'https://api.bscscan.com/api'
contract_address = w3.toChecksumAddress(address)
API_ENDPOINT = f'{url_eth}?module=contract&action=getabi&address={str(contract_address)}'
r = requests.get(url = API_ENDPOINT)
response = r.json()
abi=response['result']
contract = w3.eth.contract(address=contract_address, abi=abi)
lock_added_event = contract.events.LockAdded()

event_signature_lock_added = web3.Web3.keccak(text='LockAdded(uint256,address,address,uint256,uint256)').hex()
lock_added_event_filter = w3.eth.filter({'address': str(contract_address), 'topics': [str(event_signature_lock_added)]})

print ('Connect Status: ', w3.isConnected())
print('Abi: ', abi)

def handle_event(event):
    receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
    result = lock_added_event.processReceipt(receipt)
    print(result[0]['args'])

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)

log_loop(lock_added_event_filter, 2)
