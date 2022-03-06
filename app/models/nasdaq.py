
from xmlrpc.client import DateTime
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, time, timedelta

class Orders(BaseModel):
    symbol: str
    price: float
    shares: float
    datetime: float
    
class DayValue(BaseModel):
    day: str
    value: float

class DayResume(BaseModel):
    balance: str
    currentPrice: float
    orderDay: datetime = None
    sharePrice: float
    shares: str

class StockStatus(BaseModel):
    low: float
    high: float
    open: float
    close: float

class TradeRequest(BaseModel):
    action: str
    symbol: str
    shares: float

class TradeResponse(BaseModel):
    message: str
    price: float
    shares: float
    usdAmount: float
    
class StocksRequest(BaseModel):
    symbol: str

class StocksResponse(BaseModel):
    shares: str
    currentPrice: float
    curentValue: float
    dayValues: StockStatus
    history: List[DayResume] = None
    
class HistoricRequest(BaseModel):
    dateFrom: Optional[str]
    dateTo: Optional[str]
    symbol: str
    
class HistoricResponse(BaseModel):
    symbol: str
    values: List[DayValue] = None
