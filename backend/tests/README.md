# Naming convention of unit test methods

The name of a unit test method should have the following form:

test_[unit_of_work]_with(when)_[scenario]_should_[expected_result]
The words outside the square brackets should be kept as-is. "with" and "when" can be chosen under the situation.

The naming convention is built from 3 parts:

unit_of_work: the name of the function/route. Should be omitted if the test is gathered under a test class.
scenario: the characteristic of the arguments/payload passed to the function/route or the circumstances under which the unit of work is being executed.
expected_result: the return value/response of the function/route or the result we expect to occur after executing the unit of work. You are recommended to use the verb "return" on the return value of functions and "respond" on the response of routes.
