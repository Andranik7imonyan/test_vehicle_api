from framework import Singleton
from vehicle.models import (
                            Battery, GearShifter, BrakePedal, 
                            AccPedal, ReqTorque)


class Vehicle(metaclass=Singleton):

    @property
    def gear_shifter(self):
        return GearShifter

    @property
    def acc_pedal(self):
        return AccPedal

    @property
    def brake_pedal(self):
        return BrakePedal

    @property
    def req_torque(self):
        return ReqTorque

    @property
    def battery(self):
        return Battery
