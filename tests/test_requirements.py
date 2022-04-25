import pytest
import allure

from framework import Asserts
from framework import SoftAssertion

import tests.steps as steps
from tests.test_data import DataGenerator

from vehicle.models import Vehicle
from vehicle.constants import BatteryVoltages, ReqTorqueSignals, BrakePedalVoltages


class TestRequirements:

    def test_requirement_for_battery_when_status_is_ready(self, vehicle: Vehicle):

        """TEST ID - A1000: Set battery voltage to 'Ready' status, 
        and check that status really 'Ready', check that the rest of the 
        system has not changed their statuses. """

        battery = vehicle.battery(vehicle.battery.voltages.VOLTAGE_FOR_READY_STATUS)
        expected_all_signals = steps.get_all_signals_and_check_status_code()

        steps.update_voltage_and_check_that_signal_and_voltage_updated(battery)

        received_all_signals = steps.get_all_signals_and_check_status_code()

        with allure.step("check that all systems have not changed their "\
            + "state if we change the battery state to 'Ready'"):
            steps.check_that_all_systems_signals_is_correct(
                                                            received_all_signals,
                                                            expected_all_signals,
                                                            [battery])

    @pytest.mark.parametrize("set_battery_status_by_request", 
        [BatteryVoltages.VOLTAGE_FOR_NOT_READY_STATUS],
        indirect=["set_battery_status_by_request"])
    def test_requirement_for_battery_when_status_is_not_ready(
                                                            self, 
                                                            vehicle: Vehicle,
                                                            set_battery_status_by_request):

        """TEST ID - A1001: Set battery voltage to 'NotReady' status, 
        and check that status really 'NotReady', check that the GearPosition 
        status has become 'Neutral', check that the rest of the system 
        has not changed their statuses. """

        expected_signals = steps.get_all_signals_and_check_status_code()

        gear_shifter = vehicle.gear_shifter(
                                            vehicle.gear_shifter
                                            .gear_1_voltages
                                            .NEUTRAL_STATUS_VOLTAGE,
                                            vehicle.gear_shifter.gear_2_voltages
                                            .NEUTRAL_STATUS_VOLTAGE)
        
        steps.check_that_signal_updated(gear_shifter)

        received_signals = steps.get_all_signals_and_check_status_code()

        steps.check_that_all_systems_signals_is_correct(
                                                        received_signals, 
                                                        expected_signals,
                                                        [vehicle.battery, gear_shifter])

    @pytest.mark.parametrize("set_battery_status_by_request", 
        [BatteryVoltages.VOLTAGE_FOR_NOT_READY_STATUS],
        indirect=["set_battery_status_by_request"])
    @pytest.mark.parametrize(
                            "gear_1_voltage, gear_2_voltage", 
                            DataGenerator.generate_gear_voltages_for_park_reverse_drive())
    def test_requirement_for_battery_when_status_is_not_ready_we_cannot_switch_gear(
                                                                                    self,
                                                                                    gear_1_voltage,
                                                                                    gear_2_voltage,
                                                                                    vehicle: Vehicle,
                                                                                    set_battery_status_by_request):

        """TEST ID - A1099: Set battery voltage to 'NotReady' status, 
        and check that status really 'NotReady', check that we can't 
        switch gear. """

        gear_shifter = vehicle.gear_shifter(
                                            vehicle.gear_shifter.gear_1_voltages
                                            .NEUTRAL_STATUS_VOLTAGE, 
                                            vehicle.gear_shifter.gear_2_voltages
                                            .NEUTRAL_STATUS_VOLTAGE)

        gear_shifter.switch_gear({
                                gear_shifter.gear_1_pin_id: gear_1_voltage, 
                                gear_shifter.gear_2_pin_id: gear_2_voltage})

        steps.check_that_signal_is_correct(gear_shifter, gear_shifter.correct_signal)

        
        
    @pytest.mark.parametrize("set_battery_status_by_request", 
        [BatteryVoltages.VOLTAGE_FOR_ERROR_STATUS],
        indirect=["set_battery_status_by_request"])
    def test_requirement_for_battery_when_status_is_error(
                                                        self, 
                                                        vehicle: Vehicle, 
                                                        set_battery_status_by_request):

        """TEST ID - A1002: Set battery voltage to 'Error' status, 
        and check that status really 'Error'. All systems should shut down 
        immediately (the voltage on all pins should be set to 0), GearPosition 
        status should be 'Neutral', BrakePedal status is 'Error', 
        AccPedal status is 'Error', ReqTorque status is '0 Nm'. """

        with SoftAssertion.assert_all():

            gear_shifter = vehicle.gear_shifter(
                                                vehicle.gear_shifter.gear_1_voltages
                                                .NEUTRAL_STATUS_VOLTAGE, 
                                                vehicle.gear_shifter.gear_2_voltages
                                                .NEUTRAL_STATUS_VOLTAGE)
            
            steps.check_that_signal_updated(gear_shifter)
               
            with allure.step("check that gear_1 and gear_2 voltages is correct"):
                expected_gear_1_pin_voltage = gear_shifter.gear_1_voltages.WHEN_BATTERY_ERROR_STATUS
                expected_gear_2_pin_voltage = gear_shifter.gear_2_voltages.WHEN_BATTERY_ERROR_STATUS
                steps.check_that_pin_voltage_is_correct(
                                                            gear_shifter, 
                                                            expected_gear_1_pin_voltage, 
                                                            gear_shifter.gear_1_pin_id,
                                                            soft=True)

                steps.check_that_pin_voltage_is_correct(
                                                            gear_shifter, 
                                                            expected_gear_2_pin_voltage, 
                                                            gear_shifter.gear_2_pin_id,
                                                            soft=True)

            with allure.step("check that BrakePedal voltage and signal are correct"):
                brake_pedal = vehicle.brake_pedal()
                expected_brake_pedal_voltage = brake_pedal.voltages.WHEN_BATTERY_ERROR_STATUS
                steps.check_that_pin_voltage_is_correct(
                                                        brake_pedal, 
                                                        expected_brake_pedal_voltage, 
                                                        soft=True)

                steps.check_that_signal_is_correct(
                                                    brake_pedal,
                                                    brake_pedal.signals.ERROR,
                                                    soft=True)

            with allure.step(f"check that Accelerator"\
                 +  f"Pedal voltage and signal is correct"):
                acc_pedal = vehicle.acc_pedal()
                expected_acc_pedal_voltage = acc_pedal.voltages.WHEN_BATTERY_ERROR_STATUS
                steps.check_that_pin_voltage_is_correct(
                                                        acc_pedal, 
                                                        expected_acc_pedal_voltage, 
                                                        soft=True)

                steps.check_that_signal_is_correct(
                                                    acc_pedal,
                                                    acc_pedal.signals.ERROR,
                                                    soft=True)

            with allure.step(f"check that ReqTorque signal is correct"):
                req_torque = vehicle.req_torque()
                steps.check_that_signal_is_correct(
                                                    req_torque,
                                                    req_torque.signals.ZERO_NM,
                                                    soft=True)

            """Need fix №4, when battery voltage 'Error', Gear_1, Gear_2, 
            BrakePedal, AccPedal voltages do not match the requirements. """


    @pytest.mark.parametrize("set_any_signals_for_switching_gear", 
    DataGenerator.generate_prebaring_data_for_switching_gear(),
        indirect=["set_any_signals_for_switching_gear"])
    @pytest.mark.parametrize('gear_1_voltage, gear_2_voltage', 
    DataGenerator.generate_different_combination_voltage_for_switching_gear())
    def test_requirement_for_gear_switching_when_brake_signal_is_pressed(
                                                                        self,
                                                                        gear_1_voltage,
                                                                        gear_2_voltage,
                                                                        vehicle: Vehicle,
                                                                        set_any_signals_for_switching_gear):

        """TEST ID - A1003: Set BatteryState == "Ready", 
        BrakePedalState == "Pressed", AccPedalPos == 0%, check that 
        the statuses correspond to the set ones, switch Gear(set the appropriate voltage) 
        to Park, Neutral, Reverse, Drive, check that the gear has switched on all data sets, 
        ReqTorque signal value should be 0"""

        gear_shifter = vehicle.gear_shifter()
      
        gear_shifter.switch_gear({
                                gear_shifter.gear_1_pin_id: gear_1_voltage, 
                                gear_shifter.gear_2_pin_id: gear_2_voltage})

        req_torque = vehicle.req_torque()
        zero_nm_singal = ReqTorqueSignals.ZERO_NM
        steps.check_that_signal_is_correct(req_torque, zero_nm_singal)

    @pytest.mark.parametrize("set_any_signals_for_switching_gear", 
    DataGenerator.generate_prebaring_data_for_switching_gear(
        brake=BrakePedalVoltages.RELEASED_STATUS_VOLTAGE), 
        indirect=["set_any_signals_for_switching_gear"])
    @pytest.mark.parametrize('gear_1_voltage, gear_2_voltage', 
    DataGenerator.generate_different_combination_voltage_for_switching_gear())
    def test_requirement_for_gear_switching_when_brake_signal_is_reseased(
                                                                        self, 
                                                                        gear_1_voltage, 
                                                                        gear_2_voltage,
                                                                        vehicle: Vehicle,
                                                                        set_any_signals_for_switching_gear):

        """TEST ID - A1004: Set BatteryState == "Ready", 
        BrakePedalState == "Released", AccPedalPos == 0%, 
        check that the statuses correspond to the set ones, we can't switch 
        Gear(set the appropriate voltage) to Park, Neutral, Reverse, Drive. 
        ReqTorque can changed depending on the position of the gas pedal. """

        gear_shifter = vehicle.gear_shifter(gear_1_voltage, gear_2_voltage)

        with allure.step(f"Switch gear to gear_1={gear_1_voltage}, "\
            + f"gear_2={gear_2_voltage} voltages. No should changes"):

            gear_shifter.switch_gear(
                                    {gear_shifter.gear_1_pin_id: gear_1_voltage, 
                                    gear_shifter.gear_2_pin_id: gear_2_voltage})

            steps.check_that_signal_not_updated(gear_shifter)

        with allure.step("check that ReqTorque changes, if we press AccPedal "\
            +  "(update till 50 %), if Gear status value Drive or Reverse"):

            with allure.step("press BrakePedal"):
                baker_pedal = vehicle.brake_pedal(vehicle.brake_pedal.voltages.PRESSED_STATUS_VOLTAGE)
                steps.update_voltage_and_check_that_signal_and_voltage_updated(baker_pedal)

            gear_signal = steps.get_signal_and_check_status_code(gear_shifter)
    
            if gear_signal.value == gear_shifter.signals.DRIVE\
                or gear_signal.value == gear_shifter.signals.REVERSE:
                with allure.step("when gearShifter signal is 'Drive' "\
                    + "or 'Reverse', then switch gear"):
                    gear_shifter.switch_gear(
                                            {gear_shifter.gear_1_pin_id: gear_1_voltage, 
                                            gear_shifter.gear_2_pin_id: gear_2_voltage})

            with allure.step("release BrakePedale"):
                baker_pedal = vehicle.brake_pedal(vehicle.brake_pedal.voltages.RELEASED_STATUS_VOLTAGE)
                steps.update_voltage_and_check_that_signal_and_voltage_updated(baker_pedal)

            with allure.step("press AccPedal"):
                acc_pedal = vehicle.acc_pedal(vehicle.acc_pedal.voltages.FIFTEEN_PERCENT_STATUS_VOLTAGE)
                steps.update_voltage_and_check_that_signal_and_voltage_updated(acc_pedal)

            with allure.step("check that ReqTorque changes if Gear 'Drive' or 'Reverse'"\
                + "else if 'Park' or 'Neutral', then is is equal '0 nm'"):

                acc_signal = steps.get_signal_and_check_status_code(acc_pedal)

                req_torque = vehicle.req_torque(acc_pedal_position=acc_signal.value)
                req_torque_signal = steps.get_signal_and_check_status_code(req_torque)

                if gear_signal.value == gear_shifter.signals.PARK\
                    or gear_signal.value == gear_shifter.signals.NEUTRAL:
                    Asserts.is_equal(req_torque_signal, vehicle.req_torque.signals.ZERO_NM)
                else:
                    steps.check_that_signal_is_correct(req_torque, req_torque_signal)

    @pytest.mark.parametrize("set_any_signals_for_switching_gear", 
    DataGenerator.generate_prebaring_data_for_switching_gear(
        brake=BrakePedalVoltages.ERROR_STATUS_VOLTAGE), 
        indirect=["set_any_signals_for_switching_gear"])
    @pytest.mark.parametrize('gear_1_voltage, gear_2_voltage', 
    DataGenerator.generate_different_combination_voltage_for_switching_gear())
    def test_requirement_for_gear_switching_when_brake_signal_is_error(
        self, gear_1_voltage, gear_2_voltage, 
        set_any_signals_for_switching_gear, vehicle: Vehicle):

        """TEST ID - A1005: Set BatteryState == 'Ready', 
        BrakePedalState == "Error", AccPedalPos == 0%, 
        check that the Gear immediately went into a state of "Neutral". 
        Try to switch the gear status to Park, Drive, Reverse, we can't switch Gear. """ 

        with SoftAssertion.assert_all():
            gear_shifter = vehicle.gear_shifter(gear_1_voltage, gear_2_voltage)
            gear_shifter.switch_gear(
                                     {gear_shifter.gear_1_pin_id: gear_1_voltage, 
                                     gear_shifter.gear_2_pin_id: gear_2_voltage})

            expected_neutral_gear_signal = gear_shifter.signals.NEUTRAL

            with allure.step(f"check that gear automatically "\
                + f"switch = '{expected_neutral_gear_signal}'"):
                gear_signal = steps.get_signal_and_check_status_code(gear_shifter)

                """Need fix №2, when BrakePedalState signal value == 'Error', 
                gear is not switch automatically to 'Neutral'. """

                Asserts.is_equal(gear_signal, expected_neutral_gear_signal, soft=True)

            with allure.step("check that ReqTorque not changes,"\
                + "if we press to AccPedal (update till 100 %)"):
                acc_pedal = vehicle.acc_pedal(
                                            vehicle.acc_pedal
                                            .voltages.HUNDRED_PERCENT_STATUS_VOLTAGE)
                steps.update_voltage_and_check_that_signal_and_voltage_updated(acc_pedal)

                req_torque = vehicle.req_torque()
                zero_nm_singal = req_torque.signals.ZERO_NM

                with allure.step(f"Check that reqTorque"\
                    + f"signal is equal = {zero_nm_singal}"):
                    req_torque_signal= steps.get_signal_and_check_status_code(req_torque)
                    Asserts.is_equal(req_torque_signal, zero_nm_singal, soft=True)
        
    @pytest.mark.parametrize('acc_pedal_position', 
        DataGenerator.generate_acc_pedal_error_and_zero_status())
    def test_acc_pedal_when_not_pressed_brake_is_not_error(
                                                        self, 
                                                        acc_pedal_position,
                                                        vehicle: Vehicle):
        
        """TEST ID - A1006: Set AccPedalPosition to 'Error' or '0 %', 
        BakerPedalPosition is not 'Error' and check that 
        ReqTorque signal value is '0 Nm'. """

        expected_req_torque_signal = ReqTorqueSignals.ZERO_NM
        acc_pedal = vehicle.acc_pedal(acc_pedal_position)
        steps.update_voltage_and_check_that_signal_and_voltage_updated(acc_pedal)

        with allure.step(f"check that ReqTorque "\
            + f"signal status is = {expected_req_torque_signal}"):
            req_torque = vehicle.req_torque(vehicle.req_torque.signals.ZERO_NM)
            req_torque_signal = steps.get_signal_and_check_status_code(req_torque)
            Asserts.is_equal(req_torque_signal, expected_req_torque_signal)

    @pytest.mark.parametrize('acc_pedal_position', 
        DataGenerator.generate_acc_pedal_error_and_zero_status())
    def test_acc_pedal_when_not_pressed_and_brake_is_error(
                                                        self, 
                                                        acc_pedal_position, 
                                                        vehicle: Vehicle):

        """TEST ID - A1007: Set AccPedalPosition to 'Error' or '0 %', 
        BakerPedalPosition is 'Error' and check that ReqTorque signal value is '0 Nm'. """

        expected_req_torque_signal = ReqTorqueSignals.ZERO_NM

        acc_pedal = vehicle.acc_pedal(acc_pedal_position)
        steps.update_voltage_and_check_that_signal_and_voltage_updated(acc_pedal)

        brake_pedal = vehicle.brake_pedal(
                                        vehicle.brake_pedal
                                        .voltages.ERROR_STATUS_VOLTAGE)
        steps.update_voltage_and_check_that_signal_and_voltage_updated(brake_pedal)

        with allure.step(f"check that ReqTorque signal "\
            + f"status is {expected_req_torque_signal}"):
            req_torque = vehicle.req_torque(vehicle.req_torque.signals.ZERO_NM)
            req_torque_signal = steps.get_signal_and_check_status_code(req_torque)
            Asserts.is_equal(req_torque_signal, expected_req_torque_signal)

    @pytest.mark.parametrize("set_any_signals_for_switching_gear", 
        DataGenerator.generate_prebaring_data_for_switching_gear(
            brake=BrakePedalVoltages.PRESSED_STATUS_VOLTAGE), 
            indirect=["set_any_signals_for_switching_gear"])
    @pytest.mark.parametrize('acc_pedal_position', 
        DataGenerator.generate_acc_pedal_statuses_if_pressed())
    @pytest.mark.parametrize('gear_1_voltages, gear_2_voltages', 
        DataGenerator.generate_switching_gear_drive_and_reverse_data())
    def test_acc_pedal_when_acc_pedal_is_pressed_brake_is_pressed(
                                                                self, 
                                                                gear_1_voltages, 
                                                                gear_2_voltages, 
                                                                acc_pedal_position, 
                                                                vehicle: Vehicle,
                                                                set_any_signals_for_switching_gear):

        """TEST ID - A1008: Set AccPedalPosition > '0 %', BakerPedalPosition is 'Pressed', 
        Gear Drive or Reverse and check that ReqTorque signal value is '0 Nm'. """ 

        gear_shifter = vehicle.gear_shifter(gear_1_voltages, gear_2_voltages)
        gear_shifter.switch_gear({
                                gear_shifter.gear_1_pin_id: gear_1_voltages,
                                gear_shifter.gear_2_pin_id: gear_2_voltages})
        steps.check_that_signal_updated(gear_shifter)

        """Need fix №3, when we want set AccPedalPosition 
        pressing to '100 %', we get 'Error' statuse. """

        acc_pedal = vehicle.acc_pedal(acc_pedal_position)
        steps.update_voltage_and_check_that_signal_and_voltage_updated(acc_pedal)
        expected_req_torque_signal = ReqTorqueSignals.ZERO_NM  

        with allure.step(f"check that ReqTorque signal"\
            +  f"status is {expected_req_torque_signal}"):
            req_torque = vehicle.req_torque(vehicle.req_torque.signals.ZERO_NM)
            req_torque_signal = steps.get_signal_and_check_status_code(req_torque)
            Asserts.is_equal(req_torque_signal, expected_req_torque_signal)

    @pytest.mark.parametrize("set_any_signals_for_switching_gear", 
        DataGenerator.generate_prebaring_data_for_switching_gear(
            brake=BrakePedalVoltages.PRESSED_STATUS_VOLTAGE), 
            indirect=["set_any_signals_for_switching_gear"])
    @pytest.mark.parametrize('acc_pedal_position', 
        DataGenerator.generate_acc_pedal_statuses_if_pressed())
    @pytest.mark.parametrize('gear_1_voltages, gear_2_voltages', 
        DataGenerator.generate_switching_gear_drive_and_reverse_data())
    def test_acc_pedal_when_acc_pedal_is_pressed_brake_is_released(
                                                                self, gear_1_voltages, 
                                                                gear_2_voltages, acc_pedal_position, 
                                                                vehicle: Vehicle,
                                                                set_any_signals_for_switching_gear):

        """TEST ID - A1009: Set AccPedalPosition > '0 %', BakerPedalPosition is 'Released', 
        Gear 'Drive' or 'Reverse' and check that ReqTorque signal value is > '0 Nm'"""
        acc_pedal = vehicle.acc_pedal(acc_pedal_position)
        expected_req_torque_signal = vehicle.req_torque(acc_pedal.correct_signal)

        with allure.step(f"switch gear by voltage: gear_1"\
            + "{gear_1_voltages}, gear_2 {gear_2_voltages}, and release BrakePedal"):
            gear_shifter = vehicle.gear_shifter(gear_1_voltages, gear_2_voltages)
            gear_shifter.switch_gear({
                                    gear_shifter.gear_1_pin_id: gear_1_voltages,
                                    gear_shifter.gear_2_pin_id: gear_2_voltages})    

        brake_pedal = vehicle.brake_pedal(vehicle.brake_pedal.voltages.RELEASED_STATUS_VOLTAGE)
        steps.update_voltage_and_check_that_signal_and_voltage_updated(brake_pedal)

        """Need fix №3, when we want set AccPedalPosition 
        pressing to '100 %', we get 'Error' statuse, but we expected '10000 Nm'. """
        steps.update_voltage_and_check_that_signal_and_voltage_updated(acc_pedal)

        with allure.step(f"check that ReqTorque signal "\
            + f"status is {expected_req_torque_signal}"):
            req_torque_signal = steps.get_signal_and_check_status_code(expected_req_torque_signal)
            Asserts.is_equal(req_torque_signal, expected_req_torque_signal.correct_signal)
