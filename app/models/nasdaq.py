
from pydantic import BaseModel
from typing import Optional, List

class Orders(BaseModel):
    symbol: str
    price: float
    shares: float
    datetime: float
    
class DayValue(BaseModel):
    day: str
    value: float

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
    dateFrom: Optional[str]
    dateTo: Optional[str]
    symbol: str

class StocksResponse(BaseModel):
    dateFrom: Optional[str]
    dateTo: Optional[str]
    message: str
    price: float
    shares: float
    usdAmount: float
    buyOrders: List[Orders] = None
    
class HistoricRequest(BaseModel):
    dateFrom: Optional[str]
    dateTo: Optional[str]
    symbol: str
    
class HistoricResponse(BaseModel):
    symbol: str
    values: List[DayValue] = None