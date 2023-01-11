from tests.unit_tests.shopping_cart.test_route import (
    TestDeleteShoppingCartRoute,
    TestGetShoppingCartRoute,
    TestPostShoppingCartItemRoute,
    TestPutShoppingCartItemRoute,
    setup_item,
)


class TestDeleteShoppingCartWithMariaDB(TestDeleteShoppingCartRoute):
    pass


class TestGetShoppingCartWithMariaDB(TestGetShoppingCartRoute):
    pass


class TestPostShoppingCartItemWithMariaDB(TestPostShoppingCartItemRoute):
    pass


class TestPutShoppingCartItemWithMariaDB(TestPutShoppingCartItemRoute):
    pass
