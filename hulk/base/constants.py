from decimal import Decimal

UNIT_RATIO = 100000

PERIOD_TICK = 0
PERIOD_M1 = 1
PERIOD_M5 = 5
PERIOD_M15 = 15
PERIOD_M30 = 30
PERIOD_H1 = 60
PERIOD_H4 = 240
PERIOD_D1 = 1440
PERIOD_W1 = 10080
PERIOD_MN1 = 43200
PERIOD_CHOICES = [PERIOD_M1, PERIOD_M5, PERIOD_M15, PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1, PERIOD_W1, PERIOD_MN1]


class AccountType(object):
    REAL = 'REAL'
    DEMO = 'DEMO'
    SANDBOX = 'SANDBOX'


class OrderSide(object):
    BUY = 'BUY'
    SELL = 'SELL'


class OrderType(object):
    MARKET = "MARKET"  # A Market Order
    LIMIT = "LIMIT"  # A Limit Order
    STOP = "STOP"  # A Stop Order
    MARKET_IF_TOUCHED = "MARKET_IF_TOUCHED"  # A Market-if-touched Order
    TAKE_PROFIT = "TAKE_PROFIT"  # A Take Profit Order
    STOP_LOSS = "STOP_LOSS"  # A Stop Loss Order
    TRAILING_STOP_LOSS = "TRAILING_STOP_LOSS"  # A Trailing Stop Loss Order
    FIXED_PRICE = "FIXED_PRICE"  # A Fixed Price Order


class CancellableOrderType(object):
    LIMIT = 'LIMIT'  # A Limit Order",
    STOP = 'STOP'  # A Stop Order",
    MARKET_IF_TOUCHED = 'MARKET_IF_TOUCHED'  # A Market-if-touched Order",
    TAKE_PROFIT = 'TAKE_PROFIT'  # A Take Profit Order",
    STOP_LOSS = 'STOP_LOSS'  # A Stop Loss Order",
    TRAILING_STOP_LOSS = 'TRAILING_STOP_LOSS'  # A Trailing Stop Loss Order",


class OrderState(object):
    PENDING = 'PENDING'  # The Order is currently pending execution",
    FILLED = 'FILLED'  # The Order has been filled",
    TRIGGERED = 'TRIGGERED'  # The Order has been triggered",
    CANCELLED = 'CANCELLED'  # The Order has been cancelled",


class OrderStateFilter(object):
    PENDING = 'PENDING'  # The orders that are currently pending execution",
    FILLED = 'FILLED'  # The orders that have been filled",
    TRIGGERED = 'TRIGGERED'  # The orders that have been triggered",
    CANCELLED = 'CANCELLED'  # The orders that have been cancelled",
    ALL = 'ALL'  # The orders that are in any of the possible states: PENDING, FILLED, TRIGGERED, CANCELLED",


class TimeInForce(object):
    GTC = 'GTC'  # The Order is “Good unTil Cancelled”",
    GTD = 'GTD'  # The Order is “Good unTil Date” and will be cancelled at the provided time",
    GFD = 'GFD'  # The Order is “Good for Day” and will be cancelled at 5pm New York time",
    FOK = 'FOK'  # The Order must be immediately “Filled Or Killed”",
    IOC = 'IOC'  # The Order must be “Immediately partially filled Or Killed”",


class OrderPositionFill(object):
    OPEN_ONLY = 'OPEN_ONLY'  # When the Order is filled, only allow Positions to be opened or extended.",
    REDUCE_FIRST = 'REDUCE_FIRST'  # When the Order is filled, always fully reduce an existing Position before opening a new Position.",
    REDUCE_ONLY = 'REDUCE_ONLY'  # When the Order is filled, only reduce an existing Position.",
    DEFAULT = 'DEFAULT'  # When the Order is filled, use REDUCE_FIRST behaviour for non-client hedging Accounts, and OPEN_ONLY behaviour for client hedging Accounts."


class OrderTriggerCondition(object):
    DEFAULT = 'DEFAULT'  # Trigger an Order the “natural” way: compare its price to the ask for long Orders and bid for short Orders",
    INVERSE = 'INVERSE'  # Trigger an Order the opposite of the “natural” way: compare its price the bid for long Orders and ask for short Orders.",
    BID = 'BID'  # Trigger an Order by comparing its price to the bid regardless of whether it is long or short.",
    ASK = 'ASK'  # Trigger an Order by comparing its price to the ask regardless of whether it is long or short.",
    MID = 'MID'  # Trigger an Order by comparing its price to the midpoint regardless of whether it is long or short."


class TransactionName(object):
    """transaction name in order response"""
    orderCreateTransaction = 'orderCreateTransaction'
    longOrderCreateTransaction = 'longOrderCreateTransaction'
    shortOrderCreateTransaction = 'shortOrderCreateTransaction'
    orderFillTransaction = 'orderFillTransaction'
    longOrderFillTransaction = 'longOrderFillTransaction'
    shortOrderFillTransaction = 'shortOrderFillTransaction'
    orderCancelTransaction = 'orderCancelTransaction'
    longOrderCancelTransaction = 'longOrderCancelTransaction'
    shortOrderCancelTransaction = 'shortOrderCancelTransaction'
    orderReissueTransaction = 'orderReissueTransaction'
    orderRejectTransaction = 'orderRejectTransaction'
    orderReissueRejectTransaction = 'orderReissueRejectTransaction'
    replacingOrderCancelTransaction = 'replacingOrderCancelTransaction'

    @classmethod
    def all(cls):
        return [v for k, v in TransactionName.__dict__.items() if not k.startswith('_') and isinstance(v, str)]


class TransactionType(object):
    """type list of transaction object"""
    CREATE = 'CREATE'  # Account Create Transaction
    CLOSE = 'CLOSE'  # Account Close Transaction
    REOPEN = 'REOPEN'  # Account Reopen Transaction
    CLIENT_CONFIGURE = 'CLIENT_CONFIGURE'  # Client Configuration Transaction
    CLIENT_CONFIGURE_REJECT = 'CLIENT_CONFIGURE_REJECT'  # Client Configuration Reject Transaction
    TRANSFER_FUNDS = 'TRANSFER_FUNDS'  # Transfer Funds Transaction
    TRANSFER_FUNDS_REJECT = 'TRANSFER_FUNDS_REJECT'  # Transfer Funds Reject Transaction
    # ORDER
    MARKET_ORDER = 'MARKET_ORDER'  # Market Order Transaction
    MARKET_ORDER_REJECT = 'MARKET_ORDER_REJECT'  # Market Order Reject Transaction
    FIXED_PRICE_ORDER = 'FIXED_PRICE_ORDER'  # Fixed Price Order Transaction
    LIMIT_ORDER = 'LIMIT_ORDER'  # Limit Order Transaction
    LIMIT_ORDER_REJECT = 'LIMIT_ORDER_REJECT'  # Limit Order Reject Transaction
    STOP_ORDER = 'STOP_ORDER'  # Stop Order Transaction
    STOP_ORDER_REJECT = 'STOP_ORDER_REJECT'  # Stop Order Reject Transaction
    MARKET_IF_TOUCHED_ORDER = 'MARKET_IF_TOUCHED_ORDER'  # Market if Touched Order Transaction
    MARKET_IF_TOUCHED_ORDER_REJECT = 'MARKET_IF_TOUCHED_ORDER_REJECT'  # Market if Touched Order Reject Transaction
    TAKE_PROFIT_ORDER = 'TAKE_PROFIT_ORDER'  # Take Profit Order Transaction
    TAKE_PROFIT_ORDER_REJECT = 'TAKE_PROFIT_ORDER_REJECT'  # Take Profit Order Reject Transaction
    STOP_LOSS_ORDER = 'STOP_LOSS_ORDER'  # Stop Loss Order Transaction
    STOP_LOSS_ORDER_REJECT = 'STOP_LOSS_ORDER_REJECT'  # Stop Loss Order Reject Transaction
    TRAILING_STOP_LOSS_ORDER = 'TRAILING_STOP_LOSS_ORDER'  # Trailing Stop Loss Order Transaction
    TRAILING_STOP_LOSS_ORDER_REJECT = 'TRAILING_STOP_LOSS_ORDER_REJECT'  # Trailing Stop Loss Order Reject Transaction
    ORDER_FILL = 'ORDER_FILL'  # Order Fill Transaction
    ORDER_CANCEL = 'ORDER_CANCEL'  # Order Cancel Transaction
    ORDER_CANCEL_REJECT = 'ORDER_CANCEL_REJECT'  # Order Cancel Reject Transaction
    ORDER_CLIENT_EXTENSIONS_MODIFY = 'ORDER_CLIENT_EXTENSIONS_MODIFY'  # Order Client Extensions Modify Transaction
    ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT = 'ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT'  # Order Client Extensions Modify Reject Transaction
    # Trade
    TRADE_CLIENT_EXTENSIONS_MODIFY = 'TRADE_CLIENT_EXTENSIONS_MODIFY'  # Trade Client Extensions Modify Transaction
    TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT = 'TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT'  # Trade Client Extensions Modify Reject Transaction
    MARGIN_CALL_ENTER = 'MARGIN_CALL_ENTER'  # Margin Call Enter Transaction
    MARGIN_CALL_EXTEND = 'MARGIN_CALL_EXTEND'  # Margin Call Extend Transaction
    MARGIN_CALL_EXIT = 'MARGIN_CALL_EXIT'  # Margin Call Exit Transaction
    DELAYED_TRADE_CLOSURE = 'DELAYED_TRADE_CLOSURE'  # Delayed Trade Closure Transaction
    DAILY_FINANCING = 'DAILY_FINANCING'  # Daily Financing Transaction
    RESET_RESETTABLE_PL = 'RESET_RESETTABLE_PL'  # Reset Resettable PL Transaction



PIP_DICT = {
    # Currency
    'USDDKK': Decimal('0.0001'),
    'EURAUD': Decimal('0.0001'),
    'CHFJPY': Decimal('0.01'),
    'EURSGD': Decimal('0.0001'),
    'USDJPY': Decimal('0.01'),
    'EURTRY': Decimal('0.0001'),
    'USDCZK': Decimal('0.0001'),
    'GBPAUD': Decimal('0.0001'),
    'USDPLN': Decimal('0.0001'),
    'USDSGD': Decimal('0.0001'),
    'EURSEK': Decimal('0.0001'),
    'USDHKD': Decimal('0.0001'),
    'EURNZD': Decimal('0.0001'),
    'SGDJPY': Decimal('0.01'),
    'AUDCAD': Decimal('0.0001'),
    'GBPCHF': Decimal('0.0001'),
    'USDTHB': Decimal('0.01'),
    'TRYJPY': Decimal('0.01'),
    'CHFHKD': Decimal('0.0001'),
    'AUDUSD': Decimal('0.0001'),
    'EURDKK': Decimal('0.0001'),
    'EURUSD': Decimal('0.0001'),
    'AUDNZD': Decimal('0.0001'),
    'SGDHKD': Decimal('0.0001'),
    'EURHUF': Decimal('0.01'),
    'USDCNH': Decimal('0.0001'),
    'EURHKD': Decimal('0.0001'),
    'EURJPY': Decimal('0.01'),
    'NZDUSD': Decimal('0.0001'),
    'GBPPLN': Decimal('0.0001'),
    'GBPJPY': Decimal('0.01'),
    'USDTRY': Decimal('0.0001'),
    'EURCAD': Decimal('0.0001'),
    'USDSEK': Decimal('0.0001'),
    'GBPSGD': Decimal('0.0001'),
    'EURGBP': Decimal('0.0001'),
    'GBPHKD': Decimal('0.0001'),
    'USDZAR': Decimal('0.0001'),
    'AUDCHF': Decimal('0.0001'),
    'USDCHF': Decimal('0.0001'),
    'USDMXN': Decimal('0.0001'),
    'GBPUSD': Decimal('0.0001'),
    'EURCHF': Decimal('0.0001'),
    'EURNOK': Decimal('0.0001'),
    'AUDSGD': Decimal('0.0001'),
    'CADCHF': Decimal('0.0001'),
    'SGDCHF': Decimal('0.0001'),
    'CADHKD': Decimal('0.0001'),
    'USDINR': Decimal('0.01'),
    'NZDCAD': Decimal('0.0001'),
    'GBPZAR': Decimal('0.0001'),
    'NZDSGD': Decimal('0.0001'),
    'ZARJPY': Decimal('0.01'),
    'CADJPY': Decimal('0.01'),
    'GBPCAD': Decimal('0.0001'),
    'USDSAR': Decimal('0.0001'),
    'NZDCHF': Decimal('0.0001'),
    'NZDHKD': Decimal('0.0001'),
    'GBPNZD': Decimal('0.0001'),
    'AUDHKD': Decimal('0.0001'),
    'EURCZK': Decimal('0.0001'),
    'CHFZAR': Decimal('0.0001'),
    'USDHUF': Decimal('0.01'),
    'NZDJPY': Decimal('0.01'),
    'HKDJPY': Decimal('0.0001'),
    'CADSGD': Decimal('0.0001'),
    'USDNOK': Decimal('0.0001'),
    'USDCAD': Decimal('0.0001'),
    'AUDJPY': Decimal('0.01'),
    'EURPLN': Decimal('0.0001'),
    'EURZAR': Decimal('0.0001'),
    # METAL
    'XAUGBP': Decimal('0.01'),
    'XAGUSD': Decimal('0.0001'),
    'XAUNZD': Decimal('0.01'),
    'XAUXAG': Decimal('0.01'),
    'XAGJPY': Decimal('1'),
    'XAGHKD': Decimal('0.0001'),
    'XAGAUD': Decimal('0.0001'),
    'XAUCAD': Decimal('0.01'),
    'XAUAUD': Decimal('0.01'),
    'XAUJPY': Decimal('10'),
    'XAUHKD': Decimal('0.01'),
    'XPDUSD': Decimal('0.01'),
    'XAUUSD': Decimal('0.01'),
    'XAGCAD': Decimal('0.0001'),
    'XAUSGD': Decimal('0.01'),
    'XAGSGD': Decimal('0.0001'),
    'XAGEUR': Decimal('0.0001'),
    'XAGCHF': Decimal('0.0001'),
    'XPTUSD': Decimal('0.01'),
    'XAUCHF': Decimal('0.01'),
    'XAGNZD': Decimal('0.0001'),
    'XAGGBP': Decimal('0.0001'),
    'XAUEUR': Decimal('0.01'),
    # CFD
    'UK10YBGBP': Decimal('0.01'),
    'DE10YBEUR': Decimal('0.01'),
    'WTICOUSD': Decimal('0.01'),
    'BTCUSD': Decimal('1'),
    'NL25EUR': Decimal('0.01'),
    'CORNUSD': Decimal('0.01'),
    'SPX500USD': Decimal('1'),
    'JP225USD': Decimal('1'),
    'MBTCUSD': Decimal('0.01'),
    'USB02YUSD': Decimal('0.01'),
    'IN50USD': Decimal('1'),
    'TWIXUSD': Decimal('1'),
    'WHEATUSD': Decimal('0.01'),
    'HK33HKD': Decimal('1'),
    'US2000USD': Decimal('0.01'),
    'SUGARUSD': Decimal('0.0001'),
    'US30USD': Decimal('1'),
    'USB05YUSD': Decimal('0.01'),
    'NATGASUSD': Decimal('0.01'),
    'USB30YUSD': Decimal('0.01'),
    'SG30SGD': Decimal('0.1'),
    'AU200AUD': Decimal('1'),
    'CN50USD': Decimal('1'),
    'SOYBNUSD': Decimal('0.01'),
    'USB10YUSD': Decimal('0.01'),
    'EU50EUR': Decimal('1'),
    'FR40EUR': Decimal('1'),
    'BCOUSD': Decimal('0.01'),
    'NAS100USD': Decimal('1'),
    'DE30EUR': Decimal('1'),
    'XCUUSD': Decimal('0.0001'),
    'UK100GBP': Decimal('1'),
}
