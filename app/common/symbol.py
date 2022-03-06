import requests

async def evaluate_symbol(symbol):
    request = requests.post('https://api.nasdaq.com/api/quote/%s/info?assetclass=stocks' % (symbol))
    if request.status_code == 200:
        trade_value = request.json()
    else:
        return False