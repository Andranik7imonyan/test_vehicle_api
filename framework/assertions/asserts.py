from requests import Response

from framework.assertions.soft_assertion import SoftAssertion as SA

from typing import Any


class Asserts:

    @staticmethod
    def check_status_code(
                        response: Response, 
                        expected_status: int,
                        soft: bool = False) -> None:

        """Check the status code for compliance with the expected.
        
        @params: response object, expected status as int, type of assert. """

        actual_status = response.status_code
        result = actual_status == expected_status
        msg = f"Request error STATUS = {actual_status} "\
                + f"but expected {expected_status}. Response - {response.text}"

        if soft:
            SA.expect(result, f"SOFT: {msg}")
            return
        assert result, f" {msg}"

    @staticmethod
    def is_equal(received: Any, expected: Any, soft: bool = False) -> None:

        """Check that variables is match.

        @params: object_1, object_2, type of assert. """

        msg = f"Object is not equal. "\
                + f"Expected - {expected}, but found - {received}"

        if soft:
            SA.expect(received == expected, f"SOFT: {msg}")
            return
        assert received == expected, msg

    @staticmethod
    def is_not_equal(received: Any, expected: Any, soft: bool = False) -> None:
        msg = f"Object is equal. Expected - {expected}, but found - {received}"

        """Check that no matches in two variables.

        @params: variable_1, variable_2, type of assert. """
        
        if soft:
            SA.expect(received == expected, f"SOFT: {msg}")
            return
        assert received != expected, msg
