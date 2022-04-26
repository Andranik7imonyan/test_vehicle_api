import random


class NumberUtilities:

    @staticmethod
    def get_random_int(min: int = 0, max: int = 10) -> int:

        """Creating random integer number by range.

        @params: min possible value, max possible value. """

        return random.randint(min, max)
