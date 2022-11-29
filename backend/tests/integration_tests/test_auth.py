from tests.unit_tests.test_auth import (
    TestLoginRoute,
    TestLogoutRoute,
    TestRegisterRoute,
)


class TestLoginRouteWithMariaDB(TestLoginRoute):
    pass


class TestLogoutRouteWithMariaDB(TestLogoutRoute):
    pass


class TestRegisterRouteWithMariaDB(TestRegisterRoute):
    pass
