var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var TagSection = function (_React$Component) {
    _inherits(TagSection, _React$Component);

    function TagSection(props) {
        _classCallCheck(this, TagSection);

        var _this = _possibleConstructorReturn(this, (TagSection.__proto__ || Object.getPrototypeOf(TagSection)).call(this, props));

        _this.state = { tags: [], handler: props.handler };
        _this.click = _this.click.bind(_this);
        return _this;
    }

    _createClass(TagSection, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            $.ajax({
                url: "/tags",
                method: "GET",
                success: function (data) {
                    this.setState({ tags: data["tags"] });
                }.bind(this)
            });
        }
    }, {
        key: "click",
        value: function click(name) {
            var handler = this.state.handler;

            handler(name);
        }
    }, {
        key: "render",
        value: function render() {
            var _this2 = this;

            var tags = this.state.tags;

            array = [];

            var _loop = function _loop(i) {
                var name = tags[i]["name"];
                array.push(React.createElement(
                    "button",
                    { className: "p-2 w-full text-center", onClick: function onClick() {
                            return _this2.click(name);
                        } },
                    name
                ));
            };

            for (var i = 0; i < tags.length; i++) {
                _loop(i);
            }
            return React.createElement(
                "div",
                { className: "overflow-y-auto h-[75vh] pt-5" },
                React.createElement(
                    "div",
                    { className: "py-5" },
                    array
                ),
                React.createElement(
                    "button",
                    { className: "p-2 w-full text-center border-2", onClick: function onClick() {
                            return _this2.click(undefined);
                        } },
                    "\u6E05\u9664\u7BE9\u9078"
                )
            );
        }
    }]);

    return TagSection;
}(React.Component);

var PriceSection = function (_React$Component2) {
    _inherits(PriceSection, _React$Component2);

    function PriceSection(props) {
        _classCallCheck(this, PriceSection);

        var _this3 = _possibleConstructorReturn(this, (PriceSection.__proto__ || Object.getPrototypeOf(PriceSection)).call(this, props));

        _this3.state = {
            original_price: props.original_price,
            discount_price: props.discount_price
        };
        return _this3;
    }

    _createClass(PriceSection, [{
        key: "render",
        value: function render() {
            var _state = this.state,
                original_price = _state.original_price,
                discount_price = _state.discount_price;

            var price = [React.createElement(
                "p",
                { className: "text-center" },
                " ",
                discount_price,
                " MC "
            )];
            var discount_percentage = "-" + parseFloat(original_price / discount_price).toFixed(2) + "%";
            if (original_price != discount_price) {
                price.push(React.createElement(
                    "p",
                    { className: "text-center text-sm" },
                    React.createElement(
                        "span",
                        { className: "line-through" },
                        " ",
                        original_price,
                        " MC "
                    ),
                    React.createElement(
                        "span",
                        null,
                        "\xA0"
                    ),
                    React.createElement(
                        "span",
                        { className: "font-bold" },
                        " ",
                        discount_percentage,
                        " "
                    )
                ));
            }
            return price;
        }
    }]);

    return PriceSection;
}(React.Component);

var ItemObject = function (_React$Component3) {
    _inherits(ItemObject, _React$Component3);

    function ItemObject(props) {
        _classCallCheck(this, ItemObject);

        var _this4 = _possibleConstructorReturn(this, (ItemObject.__proto__ || Object.getPrototypeOf(ItemObject)).call(this, props));

        _this4.state = {
            id: props.id,
            detail_href: props.detail_href,
            image_href: props.image_href,
            name: props.name,
            original_price: props.original_price,
            discount_price: props.discount_price
        };
        return _this4;
    }

    _createClass(ItemObject, [{
        key: "render",
        value: function render() {
            var _state2 = this.state,
                id = _state2.id,
                detail_href = _state2.detail_href,
                image_href = _state2.image_href,
                name = _state2.name,
                original_price = _state2.original_price,
                discount_price = _state2.discount_price;

            return React.createElement(
                "a",
                { className: "h-fit w-fit", href: detail_href },
                React.createElement(
                    "div",
                    { className: "p-5 w-fit h-fit" },
                    React.createElement(
                        "div",
                        { id: "items_image_" + { id: id }, className: "w-[30vh] h-[30vh] border-2 mx-auto p-5" },
                        React.createElement("img", { className: "w-full h-full object-scale-up", src: image_href })
                    ),
                    React.createElement(
                        "p",
                        { className: "text-center p-2" },
                        " ",
                        name,
                        " "
                    ),
                    React.createElement(PriceSection, { original_price: original_price, discount_price: discount_price })
                )
            );
        }
    }]);

    return ItemObject;
}(React.Component);

var ItemSection = function (_React$Component4) {
    _inherits(ItemSection, _React$Component4);

    function ItemSection(props) {
        _classCallCheck(this, ItemSection);

        var _this5 = _possibleConstructorReturn(this, (ItemSection.__proto__ || Object.getPrototypeOf(ItemSection)).call(this, props));

        _this5.state = { item: [] };
        return _this5;
    }

    _createClass(ItemSection, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            $.ajax({
                url: "/items",
                method: "GET",
                success: function (data) {
                    if (data) {
                        this.setState({ item: data });
                    }
                }.bind(this)
            });
        }
    }, {
        key: "should_filter",
        value: function should_filter(item_data, filter_tags) {
            if (filter_tags != undefined) {
                tags = item_data["tags"];
                for (var i = 0; i < tags.length; i++) {
                    if (tags[i]["name"] == filter_tags) {
                        return true;
                    }
                }
                return false;
            }
            return true;
        }
    }, {
        key: "render",
        value: function render() {
            var item = this.state.item;

            var filter_tags = this.props.filter_tags;
            array = [];
            for (var i = 0; i < item.length; i++) {
                item_data = item[i];
                if (!this.should_filter(item_data, filter_tags)) {
                    continue;
                }
                array.push(React.createElement(ItemObject, {
                    id: item_data["id"],
                    detail_href: "/items_list/" + item_data["id"],
                    image_href: "/static/images/" + item_data["avatar"],
                    name: item_data["name"],
                    original_price: item_data["price"]["original"],
                    discount_price: item_data["price"]["discount"]
                }));
            }
            return React.createElement(
                "div",
                { className: "w-full overflow-y-auto h-[75vh] grid grid-cols-3" },
                array
            );
        }
    }]);

    return ItemSection;
}(React.Component);

var MainPlatform = function (_React$Component5) {
    _inherits(MainPlatform, _React$Component5);

    function MainPlatform(props) {
        _classCallCheck(this, MainPlatform);

        var _this6 = _possibleConstructorReturn(this, (MainPlatform.__proto__ || Object.getPrototypeOf(MainPlatform)).call(this, props));

        _this6.state = { filter_tags: undefined };
        _this6.tags_filter_handler = _this6.tags_filter_handler.bind(_this6);
        return _this6;
    }

    _createClass(MainPlatform, [{
        key: "tags_filter_handler",
        value: function tags_filter_handler(value) {
            this.setState({
                filter_tags: value
            });
        }
    }, {
        key: "render",
        value: function render() {
            var filter_tags = this.state.filter_tags;

            return React.createElement(
                "div",
                { className: "mt-20 fixed w-full" },
                React.createElement(
                    "div",
                    { className: "w-[80%] h-screen mx-auto flex flex-row gap-5 my-10" },
                    React.createElement(
                        "div",
                        { className: "w-[30%]" },
                        React.createElement(
                            "p",
                            { className: "w-full text-center p-5 text-2xl" },
                            " \u985E\u5225 "
                        ),
                        React.createElement("hr", null),
                        React.createElement(TagSection, { handler: this.tags_filter_handler })
                    ),
                    React.createElement(
                        "div",
                        { className: "w-[70%]" },
                        React.createElement(
                            "p",
                            { className: "w-full text-center p-5 text-2xl" },
                            " \u6240\u6709\u5546\u54C1 "
                        ),
                        React.createElement("hr", null),
                        React.createElement(ItemSection, { filter_tags: filter_tags })
                    )
                )
            );
        }
    }]);

    return MainPlatform;
}(React.Component);

var App = function (_React$Component6) {
    _inherits(App, _React$Component6);

    function App() {
        _classCallCheck(this, App);

        return _possibleConstructorReturn(this, (App.__proto__ || Object.getPrototypeOf(App)).apply(this, arguments));
    }

    _createClass(App, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                { className: "" },
                React.createElement(NevigationBar, null),
                React.createElement(MainPlatform, null)
            );
        }
    }]);

    return App;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("app"));
root.render(React.createElement(App, null));