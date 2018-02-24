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

instrument = 'ETH'
currency = 'AUD'
limit = 200
since_order = 0
since_trade = 0
orders = [610067267,610067457]


#Account balance
print('=== Account ==='*5)
response = client.account_balance()
pp.pprint(response)

# Trading Fee
print('=== Trading Fee ==='*5)
response = client.account_trading_fee(instrument,currency)
pp.pprint(response)

# Market data
print('=== Market Tick ==='*5)
response = client.market_tick(instrument,currency)
pp.pprint(response)
response2 = client.market_all_ticks(currency)
pp.pprint(response2)

# Orderbook
print('=== Orderbook ==='*5)
response = client.market_orderbook(instrument,currency)
pp.pprint(response)

# Market Trades
print('=== Market Trades ==='*5)
response = client.market_trades(instrument,currency)
pp.pprint(response)

# Order History
print('=== Order History ==='*5)
response = client.order_history(instrument,currency,limit,since_order)
pp.pprint(response)

# Trade History
print('=== Trade History ==='*5)
response = client.trade_history(instrument,currency,limit,since_trade)
pp.pprint(response)

# Detailed Order History
print('=== Detailed Order History ==='*5)
response = client.order_detail(orders)
pp.pprint(response)

print('=== Open Orders ==='*5)
response = client.open_orders(instrument,currency,limit,since_trade)
pp.pprint(response)

"""
#client.order_open(instrument, CURRENCY, 200, 00000000)
"""




