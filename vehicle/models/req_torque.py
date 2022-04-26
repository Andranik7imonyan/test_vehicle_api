from typing import Union

from vehicle.models.pins_manager import PinsManager
from vehicle.models.signals_manager import SignalsManager

from vehicle.constants import ReqTorqueSignals, AccPedalSignals, Constants


class ReqTorque:

    sig_id = Constants.REQ_TORQUE_SIGNAL_ID
    signals = ReqTorqueSignals
    acc_pedal_signal = AccPedalSignals

    signal_manager = SignalsManager

    def __init__(self, acc_pedal_position: Union[str, None] = None) -> None:

        if acc_pedal_position:
            match acc_pedal_position:
                case self.acc_pedal_signal.ERROR:
                    self.correct_signal = self.signals.ZERO_NM
                case self.acc_pedal_signal.ZERO_PERCENT:
                    self.correct_signal = self.signals.ZERO_NM
                case self.acc_pedal_signal.THIRDTEEN_PERCENT:
                    self.correct_signal = self.signals.THREE_THOUSAND
                case self.acc_pedal_signal.FIFTEEN_PERCENT:
                    self.correct_signal = self.signals.FIVE_THOUSAND
                case self.acc_pedal_signal.HUNDRED_PERCENT:
                    self.correct_signal = self.signals.TEN_THOUSAND
