from ....base.models import AccountType



OANDA_ENVIRONMENTS = {
    "streaming": {
        AccountType.REAL: "stream-fxtrade.oanda.com",
        AccountType.DEMO: "stream-fxpractice.oanda.com",
    },
    "api": {
        AccountType.REAL: "api-fxtrade.oanda.com",
        AccountType.DEMO: "api-fxpractice.oanda.com",
    }
}
