import web3
import requests
import time
from eth_abi import encode_abi, decode_abi
from hexbytes import HexBytes

bsc = 'https://bsc.getblock.io/mainnet/?api_key=49f921ce-971b-4fcc-acc9-bedc55da95d9'
address = '0x7ee058420e5937496F5a2096f04caA7721cF70cc'

w3 = web3.Web3(web3.HTTPProvider(bsc))

contract_address = w3.toChecksumAddress(address)

event_signature_lock_added = web3.Web3.keccak(text='LockAdded(uint256,address,address,uint256,uint256)').hex()

lock_added_event_filter = w3.eth.filter({
    'fromBlock': 14450029,
    'address': str(contract_address),
    'topics': [str(event_signature_lock_added)]
})

def get_logs_loop(poll_interval):
    latest_block_number = 0
    while True:
        logs = w3.eth.getFilterLogs(lock_added_event_filter.filter_id)
        if logs and logs[0]['blockNumber'] > latest_block_number:
            latest_block_number = logs[0]['blockNumber']

            for log in logs:
                receipt = w3.eth.getTransactionReceipt(log['transactionHash'])
                for lg in receipt.logs:
                    if HexBytes(event_signature_lock_added) in lg['topics']:
                        token, owner, amount, unlockDate = decode_abi(['address','address','uint256','uint256'], HexBytes(lg['data']))
                        print('Event Data -', ' token: ',  token, ', owner: ', owner, ', amount: ', amount, ', unlock date: ', unlockDate)
        time.sleep(poll_interval)


get_logs_loop(2)


# AttributeDict({
#     'blockHash': HexBytes('0xfa08282b1ff038bd15705bdfbc1ed540e8f5e1cec16f39f0274df77a8910a143'), 
#     'blockNumber': 14450029, 
#     'contractAddress': None, 
#     'cumulativeGasUsed': 24576805, 
#     'from': '0xBAa96149a67a919aF3a1EB2ECc189eAF5f7395F4', 
#     'gasUsed': 437596, 
#     'logs': [
#         AttributeDict({
#             'address': '0x5A3B6f18Dc79D50ab208af2fCd61D10BF7e4896F', 
#             'topics': [
#                 HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'), 
#                 HexBytes('0x000000000000000000000000baa96149a67a919af3a1eb2ecc189eaf5f7395f4'), 
#                 HexBytes('0x0000000000000000000000007ee058420e5937496f5a2096f04caa7721cf70cc')
#             ], 
#             'data': '0x00000000000000000000000000000000000000000000000000071afd498d0000', 
#             'blockNumber': 14450029, 
#             'transactionHash': HexBytes('0x95a602b9c3aebb707a4c95f9b417835e2f9c117a7ecc812d601aa4a6d12ff61a'), 
#             'transactionIndex': 184, 
#             'blockHash': HexBytes('0xfa08282b1ff038bd15705bdfbc1ed540e8f5e1cec16f39f0274df77a8910a143'), 
#             'logIndex': 514, 
#             'removed': False
#         }), 
#         AttributeDict({
#             'address': '0x5A3B6f18Dc79D50ab208af2fCd61D10BF7e4896F', 
#             'topics': [
#                 HexBytes('0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'), 
#                 HexBytes('0x000000000000000000000000baa96149a67a919af3a1eb2ecc189eaf5f7395f4'), 
#                 HexBytes('0x0000000000000000000000007ee058420e5937496f5a2096f04caa7721cf70cc')
#             ], 
#             'data': '0xfffffffffffffffffffffffffffffffffffffffffffffffffff8e502b672ffff', 
#             'blockNumber': 14450029, 
#             'transactionHash': HexBytes('0x95a602b9c3aebb707a4c95f9b417835e2f9c117a7ecc812d601aa4a6d12ff61a'), 
#             'transactionIndex': 184, 
#             'blockHash': HexBytes('0xfa08282b1ff038bd15705bdfbc1ed540e8f5e1cec16f39f0274df77a8910a143'), 
#             'logIndex': 515, 
#             'removed': False
#         }), 
#         AttributeDict({
#             'address': '0x7ee058420e5937496F5a2096f04caA7721cF70cc', 
#             'topics': [
#                 HexBytes('0x694af1cc8727cdd0afbdd53d9b87b69248bd490224e9dd090e788546506e076f'), 
#                 HexBytes('0x0000000000000000000000000000000000000000000000000000000000003952')
#             ], 
#             'data': '0x0000000000000000000000005a3b6f18dc79d50ab208af2fcd61d10bf7e4896f000000000000000000000000baa96149a67a919af3a1eb2ecc189eaf5f7395f400000000000000000000000000000000000000000000000000071afd498d00000000000000000000000000000000000000000000000000000000000063c6d8c0', 
#             'blockNumber': 14450029, 
#             'transactionHash': HexBytes('0x95a602b9c3aebb707a4c95f9b417835e2f9c117a7ecc812d601aa4a6d12ff61a'), 
#             'transactionIndex': 184, 
#             'blockHash': HexBytes('0xfa08282b1ff038bd15705bdfbc1ed540e8f5e1cec16f39f0274df77a8910a143'), 
#             'logIndex': 516, 
#             'removed': False
#         })
#     ], 
#     'logsBloom': HexBytes('0x0000000000000000008000000000000000000800000000000000000000000000000000000000000000000000000000000008000000021000000000000000020000000200000040000000002000000000000010000000000022000000000000000000000000000000000100000000000000000100000010000000000800000000000000000000000000000000000000000000000000'), 
#     'status': 1, 
#     'to': '0x7ee058420e5937496F5a2096f04caA7721cF70cc', 
#     'transactionHash': HexBytes('0x95a602b9c3aebb707a4c95f9b417835e2f9c117a7ecc812d601aa4a6d12ff61a'), 
#     'transactionIndex': 184, 
#     'type': '0x0'
# })