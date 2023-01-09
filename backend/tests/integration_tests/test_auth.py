from tests.unit_tests.auth.test_auth import (
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
