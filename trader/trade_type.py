from enum import Enum


class TradeType(Enum):
    All = 'all'
    Half = 'half'


class Action(Enum):
    Sell = 'sell'
    Buy = 'buy'
