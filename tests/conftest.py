import pytest
import allure
from pytest import Item, CallInfo, TestReport, Parser, FixtureRequest
from typing import Optional

import tests.steps as steps

from vehicle.models import SignalsManager, PinsManager, Vehicle

def pytest_addoption(parser: Parser):
    parser.addoption("--basehost", action="store", help="base url without endpoints")

@pytest.fixture(scope='session')
def vehicle():
    return Vehicle()

@pytest.fixture(scope='session', autouse=True)
def initialize_manager(request: FixtureRequest):

    """Initialize each manager. 
    We can assign a different host for each manager. """

    with allure.step("Initialize managers"):
        base_host = request.config.getoption("--basehost")
        PinsManager(base_host=base_host)
        SignalsManager(base_host=base_host)


@pytest.fixture
def set_battery_status_by_request(vehicle, request: FixtureRequest):

    battery = vehicle.battery(request.param)
    steps.update_voltage_and_check_that_signal_and_voltage_updated(battery)

@pytest.fixture
def set_any_signals_for_switching_gear(
                                    vehicle: Vehicle,
                                    request: FixtureRequest):

    """Set the initial state of the transport modules BatteryState 
    BrakePedalState, AccPedalState in accordance 
    with the parameterization of this fixture. """

    battery = vehicle.battery(request.param[0])
    steps.update_voltage_and_check_that_signal_and_voltage_updated(battery)

    brake_pedal = vehicle.brake_pedal(request.param[1])
    steps.update_voltage_and_check_that_signal_and_voltage_updated(brake_pedal)

    acc_pedal = vehicle.acc_pedal(request.param[2])
    steps.update_voltage_and_check_that_signal_and_voltage_updated(acc_pedal)

@pytest.fixture
def switch_default_data(vehicle: Vehicle):

    """Call switch_gear_by_voltage fixture, 
    and switch gear to 'Park'"""

    with allure.step("Return the gear to the Park state"\
        + "with the ability to switch gears"):
        
        battery = vehicle.battery(
                                vehicle.battery.voltages.VOLTAGE_FOR_READY_STATUS)
        steps.update_voltage_and_check_that_signal_and_voltage_updated(battery)

        brake_pedal = vehicle.brake_pedal(
                                        vehicle.brake_pedal
                                        .voltages.PRESSED_STATUS_VOLTAGE)

        steps.update_voltage_and_check_that_signal_and_voltage_updated(brake_pedal)

        acc_pedal = vehicle.acc_pedal(
                                    vehicle.acc_pedal
                                    .voltages.ZERO_PERCENT_STATUS_VOLTAGE)

        steps.update_voltage_and_check_that_signal_and_voltage_updated(acc_pedal)

        gear_shifter = vehicle.gear_shifter(
                                            vehicle.gear_shifter
                                            .gear_1_voltages.PARK_STATUS_VOLTAGE, 
                                            vehicle.gear_shifter
                                            .gear_2_voltages.PARK_STATUS_VOLTAGE)
        gear_shifter.switch_gear(
                                {gear_shifter.gear_1_pin_id: 
                                gear_shifter.gear_1_voltage, 
                                gear_shifter.gear_2_pin_id: 
                                gear_shifter.gear_2_voltage})
        
        steps.check_that_signal_updated(gear_shifter)
    yield
    with allure.step("The default state has been successfully established"):
        pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
                            item: Item, 
                            call: CallInfo[None]) -> Optional[TestReport]:

    """Display documentation of dropped tests instead of the test path. """

    outcome = yield
    report = outcome.get_result()

    test_fn = item.obj
    docstring = getattr(test_fn, '__doc__')
    if docstring:
        report.nodeid = docstring