from tests.unit_tests.tag.test_tag import (
    TestDeleteTagsByIdRoute,
    TestGetItemsByIdOfTagRoute,
    TestGetTagsByIdRoute,
    TestGetTagsRoute,
    TestPostTagsRoute,
    TestPutTagsByIdRoute,
    test_tags,  # test fixture
)


class TestDeleteTagsByIdRouteWithMariaDB(TestDeleteTagsByIdRoute):
    pass


class TestGetItemsByIdOfTagRouteWithMariaDB(TestGetItemsByIdOfTagRoute):
    pass


class TestGetTagsByIdRouteWithMariaDB(TestGetTagsByIdRoute):
    pass


class TestGetTagsRouteWithMariaDB(TestGetTagsRoute):
    pass


class TestPostTagsRouteWithMariaDB(TestPostTagsRoute):
    pass


class TestPutTagsByIdRouteWithMariaDB(TestPutTagsByIdRoute):
    pass
