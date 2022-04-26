import uuid
import string
import random


class StringUtilities:

    @staticmethod
    def get_random_id() -> str:

        """Creating a random unique UUID identifier. """

        return str(uuid.uuid4())

    @staticmethod
    def generate_random_string(length: int = 10) -> str:

        """Creating random string of the appropriate length.
        
        @param: required string length as int. """

        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        return rand_string