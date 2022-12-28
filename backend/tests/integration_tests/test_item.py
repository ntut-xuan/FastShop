from tests.unit_tests.item.test_item import (
    TestDeleteItemsByIdRoute,
    TestGetItemsByIdRoute,
    TestGetItemsCountByIdRoute,
    TestGetItemsRoute,
    TestPostItemsRoute,
    TestPutItemsByIdRoute,
    # test fixtures
    build_tags,
    setup_item,
)


class TestDeleteItemsByIdRouteWithMariaDB(TestDeleteItemsByIdRoute):
    pass


class TestGetItemsByIdRouteWithMariaDB(TestGetItemsByIdRoute):
    pass


class TestGetItemsCountByIdRouteWithTestGetItemsRoute(TestGetItemsCountByIdRoute):
    pass


class TestGetItemsRouteTestGetItemsRoute(TestGetItemsRoute):
    pass


class TestPostItemsRouteWithMariaDB(TestPostItemsRoute):
    pass


class TestPutItemsByIdRouteWithMariaDB(TestPutItemsByIdRoute):
    pass
