from typing import List

from pydantic import BaseModel


class PriceData(BaseModel):
    """Looks like: {'total': 0.2576, 'energy': 0.058, 'tax': 0.1996, 'startsAt': '2024-04-20T01:00:00.000+02:00'}"""
    total: float
    energy: float
    tax: float
    startsAt: str


class TibberData(BaseModel):
    current: PriceData
    today: List[PriceData]
    tomorrow: List[PriceData]