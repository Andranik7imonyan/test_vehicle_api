
from typing import List, Dict, Union, Any
from vehicle._interfaces import (
                                      PinVoltageFormDataBodyType, VoltageType,
                                      PinsVoltagesBodyByIdsType, IdType,
                                      PinVoltageBodyByIdType)

from vehicle.constants import (
                            Gear1Voltages, Gear2Voltages, 
                            BatteryVoltages, BrakePedalVoltages,
                            AccPedalVoltages)

from framework import NumberUtilities


class DataGenerator:

    battery_boundary_voltages = [250, 399, 400, 401, 650, 0, 799, 800, 801, 1300]

    brake_pedal_boundary_voltages = [
                                    BrakePedalVoltages.ERROR_STATUS_VOLTAGE, 
                                    0.9, 1, 1.1, 1.9, 2,
                                    BrakePedalVoltages.PRESSED_STATUS_VOLTAGE, 
                                    2.1, 2.9, 0, 3, 3.1, 
                                    BrakePedalVoltages.RELEASED_STATUS_VOLTAGE]

    @staticmethod
    def generate_update_voltage_body(
                                    value: VoltageType = None
                                    ) -> PinVoltageFormDataBodyType:
        if isinstance(value, float):
            value = str(value)
        return {
                "Voltage": (
                            None, 
                            value if value 
                            else NumberUtilities.get_random_int()
            )}

    @classmethod
    def generate_update_voltages_body_by_ids(
                                    cls, pin_id_and_voltage: Dict[IdType, VoltageType]
                                    ) -> PinsVoltagesBodyByIdsType:

        return { 
                "Pins": [cls.generate_update_voltage_body_by_id(pin_id, voltage) 
                        for pin_id, voltage in pin_id_and_voltage.items()]
        }

    @staticmethod
    def generate_update_voltage_body_by_id(
                                            pin_id: IdType, 
                                            voltage: VoltageType
                                            ) -> PinVoltageBodyByIdType:
        return {
                "PinId": pin_id,
                "Voltage": voltage
        }

    @staticmethod
    def generate_gear_voltages_for_park_reverse_drive():
            return [
                    (Gear1Voltages.PARK_STATUS_VOLTAGE, 
                    Gear2Voltages.PARK_STATUS_VOLTAGE),
                    (Gear1Voltages.REVERSE_STATUS_VOLTAGE,
                    Gear2Voltages.REVERSE_STATUS_VOLTAGE),
                    (Gear1Voltages.DRIVE_STATUS_VOLTAGE,
                    Gear2Voltages.DRIVE_STATUS_VOLTAGE)
            ]


    @staticmethod
    def generate_prebaring_data_for_switching_gear(
                                                battery = None, 
                                                brake = None, 
                                                acc = None
                                                ) -> List[List[Union[Any, VoltageType]]]:

        return [
                [battery or BatteryVoltages.VOLTAGE_FOR_READY_STATUS, 
                brake or BrakePedalVoltages.PRESSED_STATUS_VOLTAGE,
                acc or AccPedalVoltages.ZERO_PERCENT_STATUS_VOLTAGE]
            ]

    @staticmethod
    def generate_acc_pedal_error_and_zero_status() -> List[VoltageType]:
        return [
            AccPedalVoltages.ZERO_PERCENT_STATUS_VOLTAGE,
            AccPedalVoltages.ERROR_STATUS_VOLTAGE
            ]

    @staticmethod
    def generate_acc_pedal_statuses_if_pressed() -> List[VoltageType]:
        return [
                AccPedalVoltages.THIRDTEEN_PERCENT_STATUS_VOLTAGE,
                AccPedalVoltages.FIFTEEN_PERCENT_STATUS_VOLTAGE,
                AccPedalVoltages.HUNDRED_PERCENT_STATUS_VOLTAGE
            ]

      
    @staticmethod
    def generate_switching_gear_drive_and_reverse_data() -> List[List[VoltageType]]:
        return [
                [Gear1Voltages.REVERSE_STATUS_VOLTAGE, 
                Gear2Voltages.REVERSE_STATUS_VOLTAGE],
                [Gear1Voltages.DRIVE_STATUS_VOLTAGE, 
                Gear2Voltages.DRIVE_STATUS_VOLTAGE]
            ]



    @staticmethod
    def generate_different_combination_voltage_for_switching_gear() -> List[List[VoltageType]]:
        return [
                [Gear1Voltages.PARK_STATUS_VOLTAGE, 
                Gear2Voltages.PARK_STATUS_VOLTAGE], 
                [Gear1Voltages.REVERSE_STATUS_VOLTAGE, 
                Gear2Voltages.REVERSE_STATUS_VOLTAGE],
                [Gear1Voltages.NEUTRAL_STATUS_VOLTAGE, 
                Gear2Voltages.NEUTRAL_STATUS_VOLTAGE],
                [Gear1Voltages.DRIVE_STATUS_VOLTAGE, 
                Gear2Voltages.DRIVE_STATUS_VOLTAGE]
            ]
