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
