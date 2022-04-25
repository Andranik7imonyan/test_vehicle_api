from typing import Dict
from vehicle._interfaces import VoltageType, IdType

from framework import BaseManager
from tests.config import Endpoints

from tests.test_data.data_generator import DataGenerator
from vehicle.models.pin import Pin


class PinsManager(BaseManager):

    """PinsManager contains methods for managing
    'pins' (getting and updating voltage on the corresponding node Models). 
    
    NOTE: Works with models from the models/pins folder. """

    __base_path = Endpoints.BASE_PATH

    __pin_endpoint = Endpoints.PIN_ENDPOINT
    __update_pins_endpoint = Endpoints.UPDATE_PINS_ENDPOINT
    __update_pin_endpoint = Endpoints.UPDATE_PIN_ENDPOINT

    Pin: Pin = Pin

    def __init__(self, pin_id: IdType = None, **kwargs):
        super().__init__(**kwargs)
        self.pin_id = pin_id
    
    def get_pin(self, pin_id: IdType = None):
        pin_id = pin_id if pin_id else self.pin_id
        url = f'{self.__base_path}{self.__pin_endpoint}/{pin_id}'

        response = self._api_client.get(url)
        return BaseManager._check_and_set_model_data(response, self.Pin)

    def update_pin_voltage(
                            self, voltage: VoltageType, 
                            pin_id: IdType = None):

        body = DataGenerator.generate_update_voltage_body(voltage)
        if pin_id:
            self.pin_id = pin_id
        url = f"{self.__base_path}{self.__pin_endpoint}"\
            + f"/{self.pin_id}{self.__update_pin_endpoint}"

        response = self._api_client.post(url, files=body)
        return BaseManager._check_and_set_model_data(response, self.Pin)

    def update_pins_voltages(self, pin_id_and_voltages: Dict[IdType, VoltageType]):
        body = DataGenerator.generate_update_voltages_body_by_ids(pin_id_and_voltages)
        url = f"{self.__base_path}{self.__pin_endpoint}"\
            + f"{self.__update_pins_endpoint}"

        response = self._api_client.post(url, body=body)
        return BaseManager._check_and_set_model_data(response, self.Pin)
