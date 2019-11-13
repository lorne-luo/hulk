import unittest
from datetime import datetime
from decimal import Decimal
from time import sleep

from falcon.base.price import pip
from falcon.base.symbol import get_mt4_symbol

from hulk.base import AccountType, OrderSide
from hulk.broker.fxcm.account import FXCM
from . import test_config

class FXCMTestAccount(unittest.TestCase):
    """
from tests import test_config
from hulk.base import AccountType, OrderSide
from hulk.broker.fxcm.account import FXCM
account = FXCM(type=AccountType.DEMO,
                account_id=test_config.FXCM_ACCOUNT_ID,
                access_token=test_config.FXCM_ACCESS_TOKEN)
    """
    account = None
    currency = 'EUR_USD'
    tick_price = None

    def setUp(self):
        self.account = FXCM(type=AccountType.DEMO,
                            account_id=test_config.FXCM_ACCOUNT_ID,
                            access_token=test_config.FXCM_ACCESS_TOKEN)

    def tearDown(self):
        self.account.disconnect()

    def test_instrument(self):
        pass

    def test_market_order(self):
        position_count = len(self.account.open_positions)
        trade_count = len(self.account.list_open_trade())
        # market order
        order = self.account.market_order('EUR/USD', OrderSide.BUY, 0.1, take_profit=30, stop_loss=-30)
        self.assertTrue(order)
        self.assertEqual(len(self.account.open_positions), 1 + position_count)
        self.assertEqual(len(self.account.list_open_trade()), 1 + trade_count)
        self.assertTrue(len(self.account.list_all_positions()))

        trade_id = next(iter(self.account.list_open_trade()))
        trade = self.account.get_trade(trade_id)
        self.assertTrue(trade.get_amount())
        self.account.take_profit(trade_id, 40, is_in_pips=True)
        self.account.stop_loss(trade_id, -40, is_in_pips=True)

        self.account.close_trade(trade_id, 0.05)
        self.assertTrue(len(self.account.list_open_trade()) == 1 + trade_count)
        trade_id = self.account.open_trade_ids()[0]
        self.account.close_trade(trade_id)
        sleep(10)
        self.assertEqual(len(self.account.list_open_trade()), trade_count)
        self.assertEqual(len(self.account.open_positions), position_count)

        # limit stop order
        order_count = len(self.account.open_order_ids())
        order1 = self.account.limit_order('EUR/USD', OrderSide.BUY, 1.1132, 0.1, take_profit=60, stop_loss=-30)
        self.assertTrue(order1)
        order2 = self.account.stop_order('EUR/USD', OrderSide.SELL, 1.1139, 0.1, take_profit=60, stop_loss=-30)
        self.assertTrue(order2)
        self.assertEqual(len(self.account.open_order_ids()), 2 + order_count)

        self.account.take_profit(order1.get_orderId(), 40, is_in_pips=True)
        self.account.stop_loss(order2.get_orderId(), -40, is_in_pips=True)

        self.account.cancel_order(order1.get_orderId())
        self.account.cancel_order(order2.get_orderId())
        self.assertEqual(len(self.account.open_order_ids()), order_count)

        self.account.close_all_position()
        self.assertEqual(len(self.account.open_order_ids()), 0)

    def process_tick(self, data, dataframe):
        instrument = get_mt4_symbol(data['Symbol'])
        time = datetime.utcfromtimestamp(int(data['Updated']) / 1000.0)

        bid = Decimal(str(data['Rates'][0])).quantize(pip(instrument))
        ask = Decimal(str(data['Rates'][1])).quantize(pip(instrument))
        self.tick_price = data
        print(instrument, time, bid, ask)

    def test_streaming(self):
        self.account.fxcmpy.set_max_prices(4000)
        pairs = ['EUR/USD', 'GBP/USD']
        for pair in pairs:
            self.account.fxcmpy.subscribe_market_data(pair, (self.process_tick,))
            self.account.fxcmpy.subscribe_instrument(pair)

        sleep(15)
        self.assertTrue(self.tick_price)
