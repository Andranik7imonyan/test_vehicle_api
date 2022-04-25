from typing import Any

from framework import BaseModel


class Pin(BaseModel):
    
    def __init__(self, raw_data: Any) -> None:

        """Set the data according to the current model. """

        self.raw_data = raw_data
        self.pin_id = self.raw_data.get('PinId')
        self.name = self.raw_data.get("Name")
        self.voltage = self.raw_data.get("Voltage")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Pin):
            return self.voltage == other
        return self.voltage == other.voltage

    def __ne__(self, other) -> bool:
        if not isinstance(other, Pin):
                return self.voltage != other
        return self.voltage != other.voltage
