import pytest

from vehicle.models import Vehicle

from tests.test_data import DataGenerator
import tests.steps as steps

class TestBrakePedal:
    @pytest.mark.parametrize('voltage',DataGenerator.brake_pedal_boundary_voltages)
    def test_all_signals_requirements_for_brake_pedal(
                                                    self, voltage,
                                                    vehicle: Vehicle,
                                                    switch_default_data):
                                                
        """TEST ID - A1011: Set brake pedal voltage on boundary voltages - 
        (…, 0.9, 1, 1.1, 1.9, 2, 2.1, 2.9, 0, 3, 3.1, ...). 
        Check that brake pedal state changed and correct. """

        brake_pedal = vehicle.brake_pedal(voltage)
        steps.update_voltage_and_check_that_signal_and_voltage_updated(brake_pedal)
        
        """Need fix №1.1 when the voltage value is 0, the signal does
        not match the expectation. Expected - 0, but found 1.0. """
