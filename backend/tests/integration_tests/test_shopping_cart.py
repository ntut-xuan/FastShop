from tests.unit_tests.shopping_cart.test_route import (
    TestDeleteShoppingCart,
    TestGetShoppingCart,
    TestPostShoppingCartItem,
    TestPutShoppingCartItem,
    setup_item,
)


class TestDeleteShoppingCartWithMariaDB(TestDeleteShoppingCart):
    pass


class TestGetShoppingCartWithMariaDB(TestGetShoppingCart):
    pass


class TestPostShoppingCartItemWithMariaDB(TestPostShoppingCartItem):
    pass


class TestPutShoppingCartItemWithMariaDB(TestPutShoppingCartItem):
    pass
