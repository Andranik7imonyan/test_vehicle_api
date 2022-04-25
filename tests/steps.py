import allure
from http import HTTPStatus

from typing import List
from vehicle._interfaces import VoltageType, IdType, SystemsType

from framework import Asserts

from vehicle.models import Pin, SignalsManager, Signal


def get_pin_and_check_status_code(
                                    System: SystemsType,
                                    pin_id: IdType = None,
                                    expected_status_code: int = HTTPStatus.OK) -> Pin:

    with allure.step(f"get of the system '{System.__class__.__name__}' pin"):
        pin: Pin
        response, pin = System.pins_manager(System.pin_id).get_pin(pin_id)
        Asserts.check_status_code(response, expected_status_code)
        return pin

def check_that_pin_voltage_is_correct(
                                    System: SystemsType, 
                                    expected_pin_voltage: VoltageType,
                                    pin_id: IdType = None, 
                                    expected_status_code: int = HTTPStatus.OK,
                                    soft: bool = False) -> None:

    with allure.step(f"check that pin voltage of the "\
        + f"system '{SystemsType.__class__.__name__}' "\
            + f"is correct and equal {expected_pin_voltage}"):
        pin_voltage = get_pin_and_check_status_code(System, pin_id, expected_status_code)
        Asserts.is_equal(pin_voltage, expected_pin_voltage, soft)


def check_that_signal_is_correct(
                                System: SystemsType, 
                                expected_signal: str,
                                expected_status_code: int = HTTPStatus.OK,
                                soft: bool = False) -> None:

    with allure.step(f"check that signal of the "\
        + f"system '{SystemsType.__class__.__name__}' "\
            + f"is correct and equal '{expected_signal}'"):
        signal = get_signal_and_check_status_code(System, expected_status_code)
        Asserts.is_equal(signal, expected_signal, soft)


def check_that_voltage_for_system_is_correct_when_battery_error(
                                                                System: SystemsType, 
                                                                expected_status_code: int = HTTPStatus.OK,
                                                                soft: bool = False
                                                                ) -> None:
    with allure.step(f"check that the pin voltage of the '{SystemsType.__class__.__name__}' "\
        + f"is '{System.voltages.WHEN_BATTERY_ERROR_STATUS}'"):
        signal = get_pin_and_check_status_code(System, expected_status_code)
        Asserts.is_equal(signal, System.correct_signal, soft)


def get_signal_and_check_status_code(
                                    System: SystemsType, 
                                    expected_status_code: int = HTTPStatus.OK,
                                    soft: bool = False) -> Signal:

    with allure.step(f"get the system {System.__class__.__name__} signal"):
        signal: Signal
        response, signal = System.signal_manager(System.sig_id).get_signal()
        Asserts.check_status_code(response, expected_status_code, soft)
        return signal

def get_all_signals_and_check_status_code(
                                        expected_status_code: int = HTTPStatus.OK,
                                        soft: bool = False) -> Signal:

    with allure.step("get all signals"):
        signal: List[Signal]
        response, signal = SignalsManager().get_signals()
        Asserts.check_status_code(response, expected_status_code, soft)
        return signal


def update_voltage_and_check_that_signal_and_voltage_updated(
                                                            System: SystemsType, 
                                                            expected_status_code: int = HTTPStatus.OK,
                                                            pin_id : IdType = None,
                                                            soft: bool = False) -> None:
    system_name = System.__class__.__name__
    voltage = System.voltage

    with allure.step(f"updating voltage = {voltage} of "\
        + f"model name - '{system_name}'"):
        response, _ = System.pins_manager(
                                        System.pin_id)\
                                        .update_pin_voltage(voltage)

        Asserts.check_status_code(response, expected_status_code, soft)

    with allure.step(f"check that the voltage of the '{system_name}' "\
            + f"has been updated and is equal to {voltage}"):
        pin = get_pin_and_check_status_code(System, pin_id, expected_status_code)
        Asserts.is_equal(pin, voltage, soft)

        check_that_signal_updated(System, expected_status_code, soft)

def check_that_signal_updated(
                            System: SystemsType, 
                            expected_status_code: int = HTTPStatus.OK,
                            soft: bool = False) -> None:

    with allure.step(f"check that the signal of the '{SystemsType.__class__.__name__}' "\
        + f"has been updated and is equal to '{System.correct_signal}'"):
        signal = get_signal_and_check_status_code(System, expected_status_code)
        Asserts.is_equal(signal, System.correct_signal, soft)


def check_that_signal_not_updated(
                                System: SystemsType, 
                                expected_status_code: int = HTTPStatus.OK,
                                soft: bool = False) -> None:

    with allure.step(f"check that the signal of the '{SystemsType.__class__.__name__}' "\
        + f"has not been updated and is equal to '{System.correct_signal}'"):
        signal = get_signal_and_check_status_code(System, expected_status_code)
        Asserts.is_not_equal(signal, System.correct_signal, soft=soft)

def check_that_all_systems_signals_is_correct(
                                                received_signals: list,
                                                expected_signals: list,
                                                ignore_systems: List[SystemsType] = [],
                                                soft: bool = False) -> None:

    """This method compares the signals before any changes and after
    received_signals == expected_signals
        
    @params: ignore_systems - we can transfer the system we
    want to exclude from the comparison. Because why include in 
    the comparison a system whose state we specifically change. """
        
    for system in ignore_systems if ignore_systems else range(1):
        for received_signal, expected_signal in zip(received_signals, expected_signals):
            if ignore_systems:
                if received_signal.sig_id == system.sig_id\
                    and expected_signal.sig_id == system.sig_id:
                    received_signals.remove(received_signal)
                    expected_signals.remove(expected_signal)
                    continue
                else: 
                    Asserts.is_equal(received_signal, expected_signal, soft)
            else: 
                Asserts.is_equal(received_signals, expected_signals, soft)
                break
