from tests.unit_tests.models.test_model import (
    TestCascadeUpdateAndDeleteOnTagOfItem,
    TestItemOfOrder,
    TestOrder,
)


class TestCascadeUpdateAndDeleteOnTagOfItemWithMariaDB(
    TestCascadeUpdateAndDeleteOnTagOfItem
):
    pass


class TestOrderWithMariaDB(TestOrder):
    pass


class TestItemOfOrderWithMariaDB(TestItemOfOrder):
    pass
