import web3

bsc = 'https://bsc-dataseed.binance.org/'
w3 = web3.Web3(Web.HTTPProvider(bsc))
event_signature_lock_added = web3.Web3.sha3(text='LockAdded(uint256,address,address,uint256,uint256)')
event_filter = w3.eth.filter({'address': '0xb9abf98cab2c8bd2adf8282e52bf659adb0260fe', 'topics': [event_signature_lock_added]})

print (w3.isConnected())


def log_loop(handle_event, poll_interval):
    lock_added_events = w3.eth.getFilterChanges(event_filter.filter_id)
    while True:
        handle_event()
        time.sleep(poll_interval)

def get_new_events():
    new_lock_added_events = w3.eth.getFilterChanges(event_filter.filter_id)
    print('New Events: ', new_lock_added_events)


log_loop(get_new_events, 2)
