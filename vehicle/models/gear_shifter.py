from typing import Dict
from vehicle._interfaces import VoltageType, IdType

from vehicle.models.pins_manager import PinsManager
from vehicle.models.signals_manager import SignalsManager

from vehicle.constants import Constants

from vehicle.constants.data import (
                                    Gear1Voltages, Gear2Voltages, 
                                    GearShifterSignals)


class GearShifter:

    gear_1_pin_id: IdType = Constants.GEAR_1_PIN_ID
    gear_2_pin_id: IdType = Constants.GEAR_2_PIN_ID

    gear_1_voltages = Gear1Voltages
    gear_2_voltages = Gear2Voltages

    sig_id: IdType = Constants.GEAR_SIGNAL_ID
    signals = GearShifterSignals

    pins_manager = PinsManager
    signal_manager = SignalsManager

    def __init__(
                self, gear_1_voltage: VoltageType = None, 
                gear_2_voltage: VoltageType = None) -> None:

        if gear_1_voltage is not None and gear_2_voltage is not None:
            self.gear_1_voltage = gear_1_voltage
            self.gear_2_voltage = gear_2_voltage
            if gear_1_voltage == self.gear_1_voltages.PARK_STATUS_VOLTAGE and\
                 gear_2_voltage == self.gear_2_voltages.PARK_STATUS_VOLTAGE:
                self.correct_signal = self.signals.PARK
            elif gear_1_voltage == self.gear_1_voltages.NEUTRAL_STATUS_VOLTAGE and\
                 gear_2_voltage == self.gear_2_voltages.NEUTRAL_STATUS_VOLTAGE:
                self.correct_signal = self.signals.NEUTRAL
            elif gear_1_voltage == self.gear_1_voltages.REVERSE_STATUS_VOLTAGE and\
                 gear_2_voltage == self.gear_2_voltages.REVERSE_STATUS_VOLTAGE:
                self.correct_signal = self.signals.REVERSE
            elif gear_1_voltage == self.gear_1_voltages.DRIVE_STATUS_VOLTAGE and\
                 gear_2_voltage == self.gear_2_voltages.DRIVE_STATUS_VOLTAGE:
                self.correct_signal = self.signals.DRIVE
            else: 
                raise ValueError('incorrect voltages')

    def switch_gear(self, gear_ids_and_voltages: Dict[IdType, VoltageType]):
        return self.pins_manager().update_pins_voltages(gear_ids_and_voltages)

    def get_gear_1_pin(self):
        return self.pins_manager().get_pin(self.gear_1_pin_id)

    def get_gear_2_pin(self):
        return self.pins_manager().get_pin(self.gear_2_pin_id)