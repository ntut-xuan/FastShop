from tests.unit_tests.test_auth import TestLoginRoute, TestLogout, TestRegisterRoute


class TestLoginRouteWithMariaDB(TestLoginRoute):
    pass


class TestLogoutRouteWithMariaDB(TestLogout):
    pass


class TestRegisterRouteWithMariaDB(TestRegisterRoute):
    pass
