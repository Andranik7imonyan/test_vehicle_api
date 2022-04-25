import types
import inspect
from contextlib import contextmanager
from typing import List, Dict, Any, Union, Generator


class SoftAssertion:
    __failed_expectations: List[str] = []
    is_first_call: Dict[str, bool] = dict()

    @staticmethod
    def _log_failure(msg: Union[Exception, str]=None) -> None:

        """Collect each failure

        @params message strung or Exception. """

        file_path, line, funcname, contextlist = inspect.stack()[2][1:5]
        context: str = contextlist[0] if contextlist is not None else ''
        
        SoftAssertion.__failed_expectations.append(
            'Failed at "' + '%s:%s' % (file_path, line) + '", in %s()%s\n%s' % (
                funcname, ('\n\t' + 'ErrorMessage:' + '\t%s' % msg), context)
        )

    @staticmethod
    def _report_failures() -> str:

        """Report collected failures. """

        report: List[str] = []

        if SoftAssertion.__failed_expectations:
            file_path, line, funcname = inspect.stack()[2][1:4]
            report = [
                '\n\nassert_expectations() called at',
                '"%s:%s"' % (file_path, line) +
                ' in %s()\n' % funcname,
                'Failed Expectations : %s\n' %
                len(SoftAssertion.__failed_expectations)]
            for i, failure in enumerate(SoftAssertion.__failed_expectations, start=1):
                report.append('%d: %s' % (i, failure))
            SoftAssertion.__failed_expectations = []

        return '\n'.join(report)

    @staticmethod
    def expect(expr: Any, msg: str = '') -> None:

        """Keep track of failed expectations. """
        
        caller = ''

        stack_list = inspect.stack()
        for stack in stack_list:
            func_name = getattr(stack, "function", stack[3])
            if func_name.__contains__("test"):
                caller = func_name
                break

        if caller == '':
            raise Exception(
                "Could not identify test method, make sure the "
                + "call for 'expect' method is originated with 'test' method")

        if SoftAssertion.is_first_call.get(caller, True):
            SoftAssertion.__failed_expectations = []
            SoftAssertion.is_first_call[caller] = False

        """NOTE: does not support the following entry - <lambda: 
        assert 1 == 1> won't work as it's not valid lambda expression. """
        
        if isinstance(expr, types.FunctionType):
            try:
                expr()
            except Exception as exc:
                SoftAssertion._log_failure(exc)
        elif not expr:
            SoftAssertion._log_failure(msg)


    @staticmethod
    def assert_expectations() -> None:

        """Raise an assert if there are any failed expectations. """

        if SoftAssertion.__failed_expectations:
            assert False, SoftAssertion._report_failures()

    @staticmethod
    @contextmanager
    def assert_all() -> Generator:

        """Waiting for the test to complete, 
        then if there are falls, then output them. """

        try:
            yield
        finally:
            SoftAssertion.assert_expectations()
