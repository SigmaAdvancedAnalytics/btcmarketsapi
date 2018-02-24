# Dependent packages
import sys
import pprint as pp

#Local packages for testing
sys.path.append("../")
import config
from api import Client


api_key = config.api_key
private_key = config.private_key
client = Client(api_key, private_key) 

instrument = 'XRP'
currency = 'AUD'
limit = 200
since_order = 1151816479
since_trade = 1151816492
orders = [610067267,610067457]


#Account balance
print('=== Account ==='*5)
response = client.account_balance()
pp.pprint(response)


# Market data
print('=== Market Tick ==='*5)
response2 = client.market_all_ticks(currency)
pp.pprint(response2)

# Order History
print('=== Order History ==='*5)
response = client.order_history(instrument,currency,limit,since_order)
pp.pprint(response)

# Trade History
print('=== Trade History ==='*5)
response = client.trade_history(instrument,currency,limit,since_trade)
pp.pprint(response)

print('=== Open Orders ==='*5)
response = client.open_orders(instrument,currency,limit,since_trade)
pp.pprint(response)

print('=== Create Order ==='*5)
#response = client.order_create(instrument, currency, 1, 1, 'Ask', 'Limit')
#pp.pprint(response)






