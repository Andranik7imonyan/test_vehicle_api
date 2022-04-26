from requests import Session
from requests import JSONDecodeError, Response
from typing import Callable, List, Tuple, Type, Union

from framework import BaseApiClient


class BaseManager:

    """Parent of all managers. """

    def __init__(self, base_header: dict = {}, base_host: str = '') -> None:

        """Initialize BaseApi class. """

        self._api_client: Session = BaseApiClient(base_header, base_host)

    @classmethod
    def _check_and_set_model_data(
                                cls, response: Response, Model: Callable
                                ) -> Tuple[
                                            Response, 
                                            Union[object, 
                                            List[object], str]]:

        """Make sure that the data is installed 
        correctly in the transmitted model
        
        @return: response and list of model objects for which 
        need to set the data from the response 

        @params: Response, Model for to set the data. """

        data: Union[List[Type[object]], str]  = ''
        try:
            response.json()
        except JSONDecodeError:
            data = response.text
            return response, data

        if isinstance(response.json(), list):
            try:
                data = [Model(data) for data in response.json()]
            except AttributeError as e:
                raise AttributeError(e)
        else:
            try:
                data = Model(response.json())
            except AttributeError as e:
                raise AttributeError(e)
        return response, data
