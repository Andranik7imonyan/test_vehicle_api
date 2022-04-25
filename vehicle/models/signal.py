from typing import Any
from framework import BaseModel


class Signal(BaseModel):

    def __init__(self, raw_data: Any) -> None:

        """Set the data according to the current model. """

        self.raw_data = raw_data
        self.sig_id = self.raw_data.get('SigId')
        self.name = self.raw_data.get('Name')
        self.value = self.raw_data.get('Value')

    def __eq__(self, other) -> bool:
        if not isinstance(other, Signal):
            return self.value == other
        return self.value == other.value

    def __ne__(self, other) -> bool:
        if not isinstance(other, Signal):
            return self.value != other
        return self.value != other.value
