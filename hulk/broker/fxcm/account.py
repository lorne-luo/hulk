import logging
from decimal import Decimal

from falcon.base.account import AccountType
from falcon.base.order import units_to_lots
from falcon.base.price import pip
from fxcmpy import fxcmpy

from .constants import get_fxcm_symbol
from .instrument import FXCMInstrumentMixin
from .order import FXCMOrderMixin
from .position import FXCMPositionMixin
from .price import FXCMPriceMixin
from .trade import FXCMTradeMixin
from ...base.models import AccountBase
from ...utils.string import format_dict

logger = logging.getLogger(__name__)


class FXCM(FXCMPositionMixin, FXCMOrderMixin, FXCMTradeMixin, FXCMInstrumentMixin, FXCMPriceMixin, AccountBase):
    broker = 'FXCM'
    max_prices = 2000
    MAX_CANDLES = 10000

    def __init__(self, type, account_id, access_token, *args, **kwargs):
        super(FXCM, self).__init__(*args, **kwargs)
        self.type = 'real' if type == AccountType.REAL else 'demo'
        self.account_id = int(account_id)
        self.access_token = access_token
        self.pairs = self.default_pairs

        server = 'real' if type == AccountType.REAL else 'demo'

        if not access_token:
            self.fxcmpy = kwargs.get('fxcmapi')
        else:
            self.fxcmpy = fxcmpy(access_token=access_token, server=server)
        self.fxcmpy.set_max_prices(self.max_prices)

        if self.account_id != self.fxcmpy.default_account:
            self.fxcmpy.set_default_account(self.account_id)

    @property
    def summary(self):
        for account in self.fxcmpy.get_accounts('list'):
            if account['accountId'] == str(self.account_id):
                return account
        return None

    def dump(self):
        print(self.summary)

    def get_equity(self):
        summarys = self.fxcmpy.get_accounts('list')
        for s in summarys:
            if str(s.get('accountId')) == str(self.account_id):
                equity = s.get('equity')
                return Decimal(str(equity))

        raise Exception('Cant get equity.')

    def get_balance(self):
        summarys = self.fxcmpy.get_accounts('list')
        for s in summarys:
            if str(s.get('accountId')) == str(self.account_id):
                balance = s.get('balance')
                return Decimal(str(balance))

        raise Exception('Cant get balance.')

    def get_lots(self, instrument, stop_loss_pips=None, risk_ratio=Decimal('0.05')):
        max_trade = 5
        if len(self.get_trades()) >= max_trade:
            return 0

        equity = self.get_balance()
        if not stop_loss_pips:
            return equity / 1000 * Decimal('0.1')

        instrument = get_fxcm_symbol(instrument)
        pip_unit = pip(instrument)

        risk = equity * risk_ratio
        value = risk / stop_loss_pips / pip_unit

        if instrument.upper().endswith('USD'):
            price = self.get_price(instrument)
            value = value * price
        elif instrument.upper().startswith('USD'):
            lots = equity / 1000 * Decimal('0.1')
            return lots.quantize(Decimal("0.01"))
        else:
            # cross pair
            raise NotImplementedError
        units = int(value / 100) * 100
        return units_to_lots(units).quantize(Decimal("0.01"))

    def log_account(self):
        logger.info('[LOG_ACCOUNT]')
        content = format_dict(self.summary)

        logger.info(content)

    def disconnect(self):
        self.fxcmpy.close()

# if __name__ == '__main__':
#    from broker.fxcm.account import *
# fxcm = FXCM(AccountType.DEMO, settings.FXCM_ACCOUNT_ID, settings.FXCM_ACCESS_TOKEN)
