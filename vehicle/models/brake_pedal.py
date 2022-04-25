from vehicle.models.pins_manager import PinsManager
from vehicle.models.signals_manager import SignalsManager

from vehicle._interfaces import VoltageType

from vehicle.constants import Constants

from vehicle.constants import BrakePedalVoltages, BrakePedalSignals


class BrakePedal:

    pin_id = Constants.BRAKE_PEDAL_PIN_ID
    sig_id = Constants.BRAKE_PEDAL_SIGNAL_ID
    voltages = BrakePedalVoltages
    signals = BrakePedalSignals

    pins_manager = PinsManager
    signal_manager = SignalsManager

    def __init__(self, voltage: VoltageType = None) -> None:

        if voltage is not None:
            self.voltage = voltage
            if voltage < 1 or voltage >= 3:
                self.correct_signal = self.signals.ERROR
            elif 1 <= voltage < 2:
                self.correct_signal = self.signals.PRESSED
            elif 2 <= voltage < 3:
                self.correct_signal = self.signals.RELEASED
            else:
                raise ValueError('incorrect voltage')
