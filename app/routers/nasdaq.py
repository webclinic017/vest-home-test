from fastapi import APIRouter, HTTPException
import requests
from app.common import symbol
from ..models.nasdaq import *
from ..services.database import *

router = APIRouter()



def evaluate_symbol(symbol):
    request = requests.get(url ='http://api.marketstack.com/v1/eod?access_key=fe26f8f3e1722807bb9885aff7d0a88b&symbols=AAPL&limit=1')
    if request.status_code == 200:
        trade_value = request.json()
        return trade_value
    elif request.status_code == 422:
        raise HTTPException(status_code=400, detail="Symbol was not found")

    else:
        return False



@router.post("/trade", response_model=TradeResponse)
async def trade(trade: TradeRequest):
    # symbol_status = evaluate_symbol(trade.symbol)
    symbol_status = {
        "pagination": {
        "limit": 100,
        "offset": 0,
        "count": 100,
        "total": 253
        },
        "data": [
        {
        "open": 164.49,
        "high": 165.55,
        "low": 162.11,
        "close": 163.17,
        "volume": 83819592,
        "adj_high": None,
        "adj_low": None,
        "adj_close": 163.17,
        "adj_open": None,
        "adj_volume": None,
        "split_factor": 1,
        "dividend": 0,
        "symbol": "AAPL",
        "exchange": "XNAS",
        "date": "2022-03-04T00:00:00+0000"
        },
    ]}
    
    if not symbol_status or len(symbol_status["data"]) == 0:
        raise HTTPException(status_code=400, detail="Symbol data was not found")
    
    symbol_values = symbol_status["data"][0]
    if trade.action == "buy":
        date_time: str =symbol_values["date"]
        date_time = date_time[0:10]
        order = {
            "action": "buy",
            "symbol": trade.symbol,
            "price": symbol_values["open"],
            "shares": trade.shares,
            "datetime": date_time
        }
        save_order = DataBase()
        save_order.update_status(order)
        return {
            "message": "buy successful",
            "price": symbol_values["open"],
            "shares": trade.shares,
            "usdAmount": trade.shares * symbol_values["open"]
        }
    elif trade.action == "sell":
        return 200, {
            "message": "buy successful",
            "price": symbol_values["open"],
            "shares": trade.shares,
            "usdAmount": trade.shares * symbol_values["open"]
        }
    else:
        raise HTTPException(status_code=400, detail="action was not found")


@router.post("/historical-value", response_model=TradeResponse)
async def trade(trade: TradeRequest):
    # symbol_status = evaluate_symbol(trade.symbol)
    symbol_status = {
        "pagination": {
        "limit": 100,
        "offset": 0,
        "count": 100,
        "total": 253
        },
        "data": [
        {
        "open": 164.49,
        "high": 165.55,
        "low": 162.11,
        "close": 163.17,
        "volume": 83819592,
        "adj_high": None,
        "adj_low": None,
        "adj_close": 163.17,
        "adj_open": None,
        "adj_volume": None,
        "split_factor": 1,
        "dividend": 0,
        "symbol": "AAPL",
        "exchange": "XNAS",
        "date": "2022-03-04T00:00:00+0000"
        },
    ]}
    
    if not symbol_status or len(symbol_status["data"]) == 0:
        raise HTTPException(status_code=400, detail="Symbol data was not found")
    
    symbol_values = symbol_status["data"][0]
    if trade.action == "buy":
        return {
            "message": "buy successful",
            "price": symbol_values["open"],
            "shares": trade.shares,
            "usdAmount": trade.shares * symbol_values["open"]
        }
    elif trade.action == "sell":
        return 200, {
            "message": "buy successful",
            "price": symbol_values["open"],
            "shares": trade.shares,
            "usdAmount": trade.shares * symbol_values["open"]
        }
    else:
        raise HTTPException(status_code=400, detail="action was not found")

