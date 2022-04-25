from vehicle.models.pins_manager import PinsManager
from vehicle.models.signals_manager import SignalsManager
from vehicle._interfaces import VoltageType

from vehicle.constants import Constants

from vehicle.constants import BatteryVoltages, BatterySignals


class Battery:

    pin_id = Constants.BATTERY_PIN_ID
    sig_id = Constants.BATTERY_SIGNAL_ID
    voltages = BatteryVoltages
    signals = BatterySignals

    pins_manager = PinsManager
    signal_manager = SignalsManager

    def __init__(self, voltage: VoltageType = None) -> None:

        if voltage is not None:
            self.voltage = voltage
            if voltage > 800 or voltage <= 0:
                self.correct_signal = self.signals.ERROR
            elif 0 < voltage <= 400:
                self.correct_signal = self.signals.NOT_READY
            elif 800 >= voltage > 400:
                self.correct_signal = self.signals.READY
            else:
                raise ValueError('incorrect voltage')
