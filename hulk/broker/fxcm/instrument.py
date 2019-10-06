import logging

from ...base.models import InstrumentBase

logger = logging.getLogger(__name__)


class FXCMInstrumentMixin(InstrumentBase):
    _instruments = {}

    @property
    def instruments(self):
        if self._instruments:
            return self._instruments
        else:
            return self.fxcmpy.get_instruments()

    def list_instruments(self):
        """get all avaliable instruments"""
        return self.instruments
