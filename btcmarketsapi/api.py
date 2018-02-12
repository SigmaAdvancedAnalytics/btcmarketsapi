import base64, hashlib, hmac, time, urllib.request, json
from collections import OrderedDict


#Default API limit: 25 calls per 10 seconds
base_url = 'https://api.btcmarkets.net'
instruments = ['BCH','BTC','LTC','ETH','XRP','ETC']
#TODO Implement websockets - https://github.com/BTCMarkets/API/wiki/websocket
#socket_url = 'https://socket.btcmarkets.net'

# Trade values (price or volume) require this modifier - https://github.com/BTCMarkets/API/wiki/Trading-API
TRADE_MODIFIER = 100000000 #e.g. Price of $130 = 13000000000, Volume of 1 BTC = 100000000


def request(action, key, signature, timestamp, path, data):
    header = {
        'User-Agent': 'btc markets python client',
        'Accept': 'application/json', 
        'Accept-Charset': 'utf-8',  
        'Content-Type': 'application/json',
        'apikey': key,
        'timestamp': timestamp,
        'signature': signature
    }
    request = urllib.request.Request(base_url + path, data, header)
    if action == 'post':
        payload = urllib.request.urlopen(request, data.encode('utf-8'))
    else:
        payload = urllib.request.urlopen(request) 
    try:
        response = json.load(payload)
    except:
        response = {}
    return response


def get_request(key, secret, path):
    nowInMilisecond = str(int(time.time() * 1000))
    stringToSign = str(path + "\n" + nowInMilisecond + "\n").encode('utf-8')
    signature = base64.b64encode(hmac.new(secret, stringToSign, digestmod=hashlib.sha512).digest())
    return request('get', key, signature, nowInMilisecond, path, None)    


def post_request(key, secret, path, postData):
    nowInMilisecond = str(int(time.time() * 1000))
    stringToSign = str(path + "\n" + nowInMilisecond + "\n" + postData).encode('utf-8')
    signature = base64.b64encode(hmac.new(secret, stringToSign, digestmod=hashlib.sha512).digest())
    return request('post', key, signature, nowInMilisecond, path, postData)


class Client:

    def __init__(self, key, secret):
        self.key = key
        self.secret = base64.b64decode(secret)

    # Market Data - https://github.com/BTCMarkets/API/wiki/Market-data-API
    def market_tick(self,instrument,currency):
        response = get_request(self.key, self.secret, '/market/{}/{}/tick'.format(instrument.upper(),currency.upper()))
        return response

    def market_all_ticks(self,currency):
        response = []
        for instrument in instruments:
            response.append(BTCMarkets.market_tick(self,instrument,currency))
        return response

    def market_orderbook(self,instrument,currency):
        response = get_request(self.key, self.secret, '/market/{}/{}/orderbook'.format(instrument.upper(),currency.upper()))

    def market_trades(self,instrument,currency):
        response = get_request(self.key, self.secret, '/market/{}/{}/trades'.format(instrument.upper(),currency.upper()))
        return response
    
    # Account data - https://github.com/BTCMarkets/API/wiki/Account-API
    def account_balance(self):
        response = get_request(self.key, self.secret, '/account/balance')
        return response

    def account_trading_fee(self,instrument,currency):
        response = get_request(self.key, self.secret, '/account/{}/{}/tradingfee'.format(instrument.upper(),currency.upper()))
        if response:     
            response = {'instrument':instrument,'currency':currency,'tradingFeeRate':response['tradingFeeRate']/TRADE_MODIFIER}
        return response
    
    # Order Data - https://github.com/BTCMarkets/API/wiki/Trading-API
    def trade_history(self, instrument, currency, limit, since):
        data = OrderedDict([('currency', currency),('instrument', instrument),('limit', limit),('since', since)])
        postData = json.dumps(data, separators=(',', ':'))
        response = post_request(self.key, self.secret, '/order/trade/history', postData) 
        return response

    def order_history(self, instrument, currency, limit, since):
        data = OrderedDict([('currency', currency),('instrument', instrument),('limit', limit),('since', since)])
        postData = json.dumps(data, separators=(',', ':'))
        response = post_request(self.key, self.secret, '/order/history', postData) 
        return response

    def open_orders(self, instrument, currency, limit, since):
        data = OrderedDict([('currency', currency),('instrument', instrument),('limit', limit),('since', since)])
        postData = json.dumps(data, separators=(',', ':'))
        response = post_request(self.key, self.secret, '/order/open', postData) 
        return response
    
    def order_detail(self, order_ids):
        orders = {'orderIds':order_ids} 
        postData = json.dumps(orders, separators=(',', ':'))
        response = post_request(self.key, self.secret, '/order/detail', postData) 
        return response
"""
    def order_create(self, instrument, currency, price, volume, side, order_type, client_request_id):
        data = OrderedDict([('currency', currency),('instrument', instrument),
            ('price', price),('volume', volume),('orderSide', side),('ordertype', order_type),
            ('clientRequestId', client_request_id)])
        postData = json.dumps(data, separators=(',', ':'))
        return post_request(self.key, self.secret, '/order/create', postData)
"""
    
    

    