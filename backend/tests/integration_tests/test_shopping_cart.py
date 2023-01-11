from tests.unit_tests.shopping_cart.test_shopping_cart import (
    TestDeleteShoppingCartRoute,
    TestGetShoppingCartRoute,
    TestPostShoppingCartItemRoute,
    TestPutShoppingCartItemRoute,
    setup_item,
)


class TestDeleteShoppingCartRouteWithMariaDB(TestDeleteShoppingCartRoute):
    pass


class TestGetShoppingCartRouteWithMariaDB(TestGetShoppingCartRoute):
    pass


class TestPostShoppingCartItemRouteWithMariaDB(TestPostShoppingCartItemRoute):
    pass


class TestPutShoppingCartItemRouteWithMariaDB(TestPutShoppingCartItemRoute):
    pass
