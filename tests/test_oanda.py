import unittest
from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from pandas import DataFrame
from v20.transaction import LimitOrderTransaction, OrderCancelTransaction, StopOrderTransaction

from hulk.base import OrderSide, PERIOD_M5, pip, calculate_price
from hulk.broker.oanda.account import OANDA
from hulk.broker.oanda.common.prints import print_positions
from . import test_config


class OANDATestAccount(unittest.TestCase):
    """
from tests import test_config
from hulk.base import AccountType, OrderSide
from hulk.broker.fxcm.account import FXCM
from hulk.broker.oanda.account import OANDA
from hulk.base import OrderSide, PERIOD_M5, pip, calculate_price
from decimal import Decimal
from datetime import datetime
from dateutil.relativedelta import relativedelta
account = OANDA(type='DEMO',
         account_id=test_config.OANDA_ACCOUNT_ID,
         access_token=test_config.OANDA_ACCESS_TOKEN,
         application_name='test app')
    """
    account = None
    currency = 'EUR_USD'

    def setUp(self):
        self.account = OANDA(type='DEMO',
                             account_id=test_config.OANDA_ACCOUNT_ID,
                             access_token=test_config.OANDA_ACCESS_TOKEN,
                             application_name='test app')

    def test_instrument(self):
        # list_instruments
        instruments = self.account.list_instruments()
        self.assertTrue(isinstance(instruments, dict))
        print(instruments[self.currency])

        # pip unit
        pip_unit = pip(self.currency)
        self.assertEqual(pip_unit, Decimal('0.0001'))
        pips = pip(self.currency, 0.00315)
        self.assertEqual(pips, 31.5)

        # calculate_price
        price = calculate_price(1.11325, OrderSide.BUY, 31.4, self.currency)
        self.assertEqual(price, Decimal('1.11639'))

        # get_candle
        minutes = 101
        to_time = datetime.utcnow() - relativedelta(hours=24)
        from_time = to_time - relativedelta(minutes=minutes)
        count = int(minutes / PERIOD_M5)

        # get_candle
        candles = self.account.get_candle(self.currency, PERIOD_M5, fromTime=from_time, toTime=to_time)
        self.assertTrue(isinstance(candles, DataFrame))

    def test_position(self):
        # pull_position
        position = self.account.pull_position(self.currency)
        print_positions([position])

        # list_all_positions
        positions = self.account.list_all_positions()
        print_positions(positions)

        # list_open_positions
        positions = self.account.list_open_positions()
        print_positions(positions)

        # close_position
        detail = self.account.close_position(self.currency)
        self.assertTrue(detail)

        # close_all_position
        self.account.close_all_position()

    def test_market_order(self):
        self.account.list_prices(['EUR_USD', 'GBP_USD', ])
        self.assertTrue(len(self.account._prices))
        ask = self.account._prices.get(self.currency).get('ask')
        tp_price = calculate_price(ask, OrderSide.BUY, 31.4, self.currency)

        trades = self.account.list_trade()
        trade_exists = len(trades)

        transactions = self.account.market_order(self.currency, OrderSide.BUY, lots=0.1,
                                                 take_profit=tp_price, stop_loss=40)
        self.assertTrue(transactions)

        trades = self.account.list_trade()
        self.assertEqual(len(trades), trade_exists + 1)

        trades = self.account.list_open_trade()
        self.assertTrue(len(trades))

        trade_id = trades[0].id
        transactions = self.account.take_profit(trade_id, price='1.33322')
        self.assertTrue(transactions)

        trade = self.account.get_trade(trade_id)
        self.assertTrue(trade)

        order = self.account.get_order(trade.takeProfitOrder.id)
        self.assertTrue(order)

        orders = self.account.list_order()
        self.assertTrue(orders)

        transactions = self.account.take_profit(trade_id, order_id=trade.takeProfitOrder.id, price='1.44444')
        self.assertTrue(transactions)

        transactions = self.account.trailing_stop_loss(trade_id=trade_id, pips=40.1)
        self.assertTrue(transactions)

        transactions = self.account.close(trade_id, lots=0.04)
        self.assertTrue(transactions)
        transactions = self.account.close(trade_id)
        self.assertTrue(transactions)
        self.assertFalse(trade_id in self.account.trades)

    def test_pending_order(self):
        self.account.list_prices()
        self.assertTrue(len(self.account._prices))
        ask = self.account._prices.get(self.currency).get('ask')
        limit_price = calculate_price(ask, OrderSide.BUY, 31.4, self.currency)

        transactions = self.account.limit_order(self.currency, OrderSide.SELL, price=limit_price, lots=0.1)
        self.assertTrue(transactions)
        self.assertTrue(isinstance(transactions[0], LimitOrderTransaction))

        transaction = self.account.cancel_order(transactions[0].id)
        self.assertTrue(isinstance(transaction, OrderCancelTransaction))
        self.assertTrue(transaction.id not in self.account.orders)

        transactions = self.account.stop_buy(self.currency, price=limit_price, lots=0.1)
        self.assertTrue(isinstance(transactions[0], StopOrderTransaction))

        transaction = self.account.cancel_order(transactions[0].id)
        self.assertTrue(isinstance(transaction, OrderCancelTransaction))
        self.assertTrue(transaction.id not in self.account.orders)
