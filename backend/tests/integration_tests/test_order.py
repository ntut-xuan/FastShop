from tests.unit_tests.order.test_order import (
    TestDeleteOrdersByIdRoute,
    TestGetOrdersByIdRoute,
    TestGetOrdersRoute,
    TestPostOrdersRoute,
)


class TestDeleteOrdersByIdRouteWithMariaDB(TestDeleteOrdersByIdRoute):
    pass


class TestGetOrdersByIdRouteWithMariaDB(TestGetOrdersByIdRoute):
    pass


class TestGetOrdersRouteWithMariaDB(TestGetOrdersRoute):
    pass


class TestPostOrdersRouteWithMariaDB(TestPostOrdersRoute):
    pass
