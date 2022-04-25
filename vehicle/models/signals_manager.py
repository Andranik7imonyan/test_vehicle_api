from framework import BaseManager
from vehicle._interfaces import IdType

from tests.config import Endpoints
from vehicle.models.signal import Signal


class SignalsManager(BaseManager):

    """SignalsManager contains methods for managing
    'signals' (getting signals on the corresponding node Models). 
    
    NOTE: Works with models from the models/signals folder. """

    base_path = Endpoints.BASE_PATH
    signal_endpoint = Endpoints.SIGNAL_ENDPOINT

    Signal: Signal = Signal

    def __init__(self, sig_id: IdType = None, **kwargs):
        super().__init__(**kwargs)
        self.sig_id = sig_id

    def get_signal(self):
        url = f'{self.base_path}{self.signal_endpoint}/{self.sig_id}'
        response = self._api_client.get(url)
        return BaseManager._check_and_set_model_data(response, self.Signal)

    def get_signals(self):
        url = f'{self.base_path}{self.signal_endpoint}'
        response = self._api_client.get(url)
        return BaseManager._check_and_set_model_data(response, self.Signal)
