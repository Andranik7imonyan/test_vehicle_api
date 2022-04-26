import allure
import requests
from requests import Response, Session

from framework.utilities.singleton import Singleton


class BaseApiClient(metaclass=Singleton):

    def __init__(
                self, base_header: dict, 
                base_host: str) -> None:

        """Initialize API session, base header, base host"""
        
        self.__session: Session = requests.session()
        self.base_header = base_header
        self.base_host = base_host

    def get(
            self, url: str, 
            headers: dict = {}, **kwargs) -> Response:

        """Get request"""

        url = f"{self.base_host}{url}"
        with allure.step(f"Send GET request to url - {url}"):
            response = self.__session.get(
                url, headers=headers or self.base_header, **kwargs)
        return response

    def post(
            self, url: str, body: dict = {}, 
            headers: dict = {}, **kwargs) -> Response:

        """Post request: if you need to pass 'form-data' as 
        the body, then pass it to the 'files' parameter. """

        url = f"{self.base_host}{url}"
        body = kwargs.get('files') or body
        with allure.step(f"Send POST request to url - {url} with body {body}"):
            response = self.__session.post(
                url, headers=headers or self.base_header, json=body, **kwargs)
        return response
