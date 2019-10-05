from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta, MO

from .constants import (UNIT_RATIO, PERIOD_M1, PERIOD_M5, PERIOD_M15, PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1,
                        PERIOD_W1, PERIOD_MN1, PIP_DICT, OrderSide)


def get_timeframe_name(timeframe_value):
    if timeframe_value == PERIOD_M1:
        return 'M1'
    if timeframe_value == PERIOD_M5:
        return 'M5'
    if timeframe_value == PERIOD_M15:
        return 'M15'
    if timeframe_value == PERIOD_M30:
        return 'M30'
    if timeframe_value == PERIOD_H1:
        return 'H1'
    if timeframe_value == PERIOD_H4:
        return 'H4'
    if timeframe_value == PERIOD_D1:
        return 'D1'
    if timeframe_value == PERIOD_W1:
        return 'W1'
    if timeframe_value == PERIOD_MN1:
        return 'MN1'
    raise Exception('unsupport timeframe')


def get_mt4_symbol(symbol):
    symbol = str(symbol)
    return symbol.replace(' ', '').replace('_', '').replace('-', '').replace('/', '')


def pip(symbol, price=None, _abs=False):
    symbol = get_mt4_symbol(symbol)
    if symbol not in PIP_DICT:
        raise Exception('%s not in PIP_DICT.' % symbol)

    pip_unit = PIP_DICT[symbol]
    if price:
        price = Decimal(str(price))
        if _abs:
            price = abs(price)
        return (price / pip_unit).quantize(Decimal("0.1"))

    return pip_unit


def profit_pip(symbol, open, close, side, abs=False):
    open = Decimal(str(open))
    close = Decimal(str(close))
    if side == OrderSide.BUY:
        profit = close - open
    else:
        profit = open - close

    return pip(symbol, profit)


def calculate_price(base_price, side, pip, instrument):
    instrument = get_mt4_symbol(instrument)
    pip_unit = pip(instrument)
    base_price = Decimal(str(base_price))
    pip = Decimal(str(pip))

    if side == OrderSide.BUY:
        return base_price + pip * pip_unit
    elif side == OrderSide.SELL:
        return base_price - pip * pip_unit


def get_candle_time(time, timeframe):
    t = time.replace(second=0, microsecond=0)

    if timeframe in [PERIOD_M1, PERIOD_M5, PERIOD_M15, PERIOD_M30]:
        minute = t.minute // timeframe * timeframe
        return t.replace(minute=minute)
    if timeframe in [PERIOD_H1, PERIOD_H4]:
        t = t.replace(minute=0)
        hourframe = int(timeframe / 60)
        hour = t.hour // hourframe * hourframe
        return t.replace(hour=hour)
    if timeframe in [PERIOD_D1]:
        return t.replace(hour=0, minute=0)
    if timeframe in [PERIOD_W1]:
        monday = time + relativedelta(weekday=MO(-1))
        return monday.replace(hour=0, minute=0, second=0, microsecond=0)
    if timeframe in [PERIOD_MN1]:
        return t.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    raise NotImplementedError


def units_to_lots(units):
    units = Decimal(str(units))
    return units / UNIT_RATIO


def lots_to_units(lot, side=OrderSide.BUY):
    try:
        lot = Decimal(str(lot)).quantize(Decimal('0.01'))
    except:
        return None

    if side == OrderSide.BUY:
        return lot * UNIT_RATIO
    elif side == OrderSide.SELL:
        return lot * UNIT_RATIO * -1
    raise Exception('Unknow direction.')


def is_market_open():
    now = datetime.utcnow()

    close_hour = 19
    open_hour = 22

    HOLIDAY = [(1, 1)]
    if now.weekday() == 5:
        return False
    if now.weekday() == 4:
        return now.hour < close_hour
    if now.weekday() == 6:
        return now.hour > open_hour

    for date in HOLIDAY:
        next_day = now + relativedelta(hours=24)
        if (next_day.day, next_day.month) == date:
            return next_day.hour < close_hour

        if (now.day, now.month) == date:
            return now.hour > open_hour
    return True
