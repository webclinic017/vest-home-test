
from pydantic import BaseModel
from typing import Optional

class TradeRequest(BaseModel):
    action: str
    symbol: str
    shares: float

class TradeResponse(BaseModel):
    message: str
    price: float
    shares: float
    usdAmount: float