import pytest

from tests.test_data import DataGenerator
import tests.steps as steps

class TestBattery:

    @pytest.mark.parametrize('voltage', DataGenerator.battery_boundary_voltages)
    def test_battery_signals_at_voltage_boundary_voltages(
                                                        self,vehicle,
                                                        voltage, 
                                                        switch_default_data):
                                                
        """TEST ID - A1010: Set battery voltage on boundary voltages - 
        (399, 400, 401, 650, 0, 799, 800, 801). Check that battery state is correct. 
        Battery state is correct, on each data set. """

        battery = vehicle.battery(voltage)
        steps.update_voltage_and_check_that_signal_and_voltage_updated(battery)

        """Need fix №1 when the voltage value is 0, the signal does
        not match the expectation. Expected - Error, but found NotReady. 
        Also, the system does not allow you to set the voltage to 0. """
