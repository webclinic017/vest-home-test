from xmlrpc.client import boolean
from fastapi import APIRouter, HTTPException
import requests
from ..models.nasdaq import *
from ..services.database import *

router = APIRouter()

def evaluate_symbol(data, today: bool = False):
    symbol: str = data["symbol"]
    date_from = ""
    date_to = ""
    if "dateFrom" in data and data["dateFrom"]:
        date_from = "&date_from=" +  data["dateFrom"]
        
    if "dateTo" in data and data["dateTo"]:
        date_to = "&date_to=" + data["dateTo"]
    url ='http://api.marketstack.com/v1/eod?access_key=fe26f8f3e1722807bb9885aff7d0a88b&symbols={}{}{}'.format(
            symbol.upper(), 
            date_from, 
            date_to
    )
    
    if today == True:
        url ='http://api.marketstack.com/v1/eod?access_key=fe26f8f3e1722807bb9885aff7d0a88b&symbols={}&limit=1'.format(
            symbol.upper()
        )
    request = requests.get(url=url)
    if request.status_code == 200:
        trade_value = request.json()
        return trade_value
    elif request.status_code == 422:
        raise HTTPException(status_code=400, detail="Symbol was not found")

    else:
        return False



@router.post("/trade", response_model=TradeResponse)
async def trade(trade: TradeRequest):
    evaluate = {
        "symbol": trade.symbol,
        "action": trade.action,
        "shares": trade.shares
    }
    symbol_status = evaluate_symbol(evaluate, today=True)
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
        date_time: str =symbol_values["date"]
        date_time = date_time[0:10]
        order = {
            "action": "sell",
            "symbol": trade.symbol,
            "price": symbol_values["open"],
            "shares": trade.shares,
            "datetime": date_time
        }
        save_order = DataBase()
        save_order.update_status(order)
        return {
            "message": "sell successful",
            "price": symbol_values["open"],
            "shares": trade.shares,
            "usdAmount": trade.shares * symbol_values["open"]
        }
    else:
        raise HTTPException(status_code=400, detail="action was not found")


@router.post("/list-stocks", response_model=StocksResponse)
async def view_history(history: StocksRequest):
    evaluate = {
        "symbol": history.symbol,
    }
    evaluate_today = evaluate_symbol(evaluate, True)

    
    if not evaluate_today or len(evaluate_today["data"]) == 0:
        raise HTTPException(status_code=400, detail="Symbol data was not found")
    
    symbol_values = evaluate_today["data"][0]
    get_status = DataBase()
    status = get_status.get_status({
        "symbol": history.symbol,
    })
    day_values = []
    for symbol_value in status["historical"]:
        balance = 100 - (
                float(symbol_values["open"])* 100 / 
                float(symbol_value["price"])
            )
        day_values.append({
            "balance": str(round(balance, 2)) + "%",
            "currentPrice": symbol_values["open"],
            "orderDay": str(symbol_value["datetime"]),
            "sharePrice": symbol_value["price"],
            "shares": symbol_value["shares"]
        })
        
    response = {
        "shares": status["shares"]["amount"],
        "currentPrice":  symbol_values["open"],
        "curentValue": status["shares"]["amount"] * symbol_values["open"],
        "dayValues":{
            "low": symbol_values["low"],
            "high": symbol_values["high"],
            "open": symbol_values["open"],
            "close": symbol_values["close"]
        },
        "history": day_values
    }
    return response


@router.post("/historic-price", response_model=HistoricResponse)
async def view_history(history: HistoricRequest):
    evaluate = {
        "symbol": history.symbol,
        "dateTo": history.dateTo,
        "dateFrom": history.dateFrom
    }
    symbol_status = evaluate_symbol(evaluate)
    if not symbol_status or len(symbol_status["data"]) == 0:
        raise HTTPException(status_code=400, detail="Symbol data was not found")
    
    symbol_values = symbol_status["data"]
    day_values = []
    for symbol_value in symbol_values:
        day_values.append({
            "day": symbol_value["date"][0:10],
            "value": symbol_value["close"]
        })
    
    response: HistoricResponse = {
        "symbol": history.symbol,
        "values": day_values
    }
    return response