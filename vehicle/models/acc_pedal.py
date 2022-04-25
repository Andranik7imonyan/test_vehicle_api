from vehicle.models.pins_manager import PinsManager
from vehicle.models.signals_manager import SignalsManager
from vehicle._interfaces import VoltageType

from vehicle.constants import Constants
from vehicle.constants import AccPedalSignals, AccPedalVoltages

class AccPedal:

    pin_id = Constants.ACC_PEDAL_PIN_ID
    sig_id = Constants.ACC_PEDAL_SIGNAL_ID
    voltages = AccPedalVoltages
    signals = AccPedalSignals

    pins_manager = PinsManager
    signal_manager = SignalsManager

    def __init__(self, voltage: VoltageType = None) -> None:

        if voltage is not None:
            self.voltage = voltage
            if voltage < 1 or voltage >= 3.5:
                self.correct_signal = self.signals.ERROR
            elif 1 <= voltage < 2:
                self.correct_signal = self.signals.ZERO_PERCENT
            elif 2 <= voltage < 2.5:
                self.correct_signal = self.signals.THIRDTEEN_PERCENT
            elif 2.5 <= voltage < 3:
                    self.correct_signal = self.signals.FIFTEEN_PERCENT
            elif 3 <= voltage < 3.5:
                    self.correct_signal = self.signals.HUNDRED_PERCENT
