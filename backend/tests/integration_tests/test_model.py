from tests.unit_tests.models.test_model import (
    TestCascadeUpdateAndDeleteOnTagOfItem,
    TestItemOfOrder,
    TestOrder,
    TestShoppingCart,
)


class TestCascadeUpdateAndDeleteOnTagOfItemWithMariaDB(
    TestCascadeUpdateAndDeleteOnTagOfItem
):
    pass


class TestShoppingCartWithMariaDB(TestShoppingCart):
    pass


class TestOrderWithMariaDB(TestOrder):
    pass


class TestItemOfOrderWithMariaDB(TestItemOfOrder):
    pass
