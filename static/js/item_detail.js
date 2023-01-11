var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var PriceComponent = function (_React$Component) {
    _inherits(PriceComponent, _React$Component);

    function PriceComponent(props) {
        _classCallCheck(this, PriceComponent);

        var _this = _possibleConstructorReturn(this, (PriceComponent.__proto__ || Object.getPrototypeOf(PriceComponent)).call(this, props));

        _this.state = {
            original_price: props.original_price,
            discount_price: props.discount_price
        };
        return _this;
    }

    _createClass(PriceComponent, [{
        key: "render",
        value: function render() {
            original_price = this.props.original_price;
            discount_price = this.props.discount_price;
            if (discount_price != original_price) {
                return React.createElement(
                    "p",
                    { className: "md:text-base xl:text-2xl font-serif" },
                    React.createElement(
                        "span",
                        { className: "pr-5" },
                        " NT$ ",
                        discount_price,
                        " "
                    ),
                    React.createElement(
                        "span",
                        { className: "pr-5 font-bold text-gray-400 line-through" },
                        " NT$ ",
                        original_price,
                        " "
                    ),
                    React.createElement(
                        "span",
                        { className: "pr-5 font-bold" },
                        " - ",
                        parseFloat((original_price - discount_price) * 100 / original_price).toFixed(2),
                        " % "
                    )
                );
            } else {
                return React.createElement(
                    "p",
                    { className: "md:text-base xl:text-2xl font-serif" },
                    React.createElement(
                        "span",
                        { className: "pr-5" },
                        " NT$ ",
                        original_price,
                        " "
                    )
                );
            }
        }
    }]);

    return PriceComponent;
}(React.Component);

var MainPlatform = function (_React$Component2) {
    _inherits(MainPlatform, _React$Component2);

    function MainPlatform(props) {
        _classCallCheck(this, MainPlatform);

        var _this2 = _possibleConstructorReturn(this, (MainPlatform.__proto__ || Object.getPrototypeOf(MainPlatform)).call(this, props));

        _this2.state = {
            image_href: undefined,
            name: undefined,
            count: undefined,
            original_price: undefined,
            discount_price: undefined,
            description: ""
        };
        _this2.increase_count = _this2.increase_count.bind(_this2);
        return _this2;
    }

    _createClass(MainPlatform, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            item_id = window.location.pathname.split("/")[2];
            $.ajax({
                url: "/items/" + item_id,
                method: "GET",
                success: function (data) {
                    this.setState({
                        image_href: "/static/images/" + data["avatar"],
                        name: data["name"],
                        count: data["count"],
                        original_price: data["price"]["original"],
                        discount_price: data["price"]["discount"],
                        description: data["description"]
                    });
                }.bind(this),
                error: function (data) {
                    window.location.href = "/items_list";
                }.bind(this)
            });
        }
    }, {
        key: "newline_map_description",
        value: function newline_map_description(description) {
            if (description == undefined) {
                return "";
            } else {
                return description.split("\\n").map(function (item, idx) {
                    return React.createElement(
                        React.Fragment,
                        { key: idx },
                        item,
                        React.createElement("br", null)
                    );
                });
            }
        }
    }, {
        key: "increase_count",
        value: function increase_count() {
            var count = this.state.count;

            var value = document.getElementById("order_count_input").value;
            var int_value = parseInt(value);
            if (isNaN(int_value)) {
                int_value = 0;
            }
            int_value = Math.min(int_value + 1, count);
            document.getElementById("order_count_input").value = int_value;
        }
    }, {
        key: "decrease_count",
        value: function decrease_count() {
            var value = document.getElementById("order_count_input").value;
            var int_value = parseInt(value);
            if (isNaN(int_value)) {
                int_value = 0;
            }
            int_value = Math.max(int_value - 1, 0);
            document.getElementById("order_count_input").value = int_value;
        }
    }, {
        key: "get_count_of_item_from_shopping_cart",
        value: function get_count_of_item_from_shopping_cart() {
            var id = parseInt(window.location.pathname.split("/")[2]);
            var count = 0;
            $.ajax({
                url: "/shopping_cart",
                type: "GET",
                async: false,
                success: function success(data) {
                    for (var i = 0; i < data["count"]; i++) {
                        if (data["items"][i]["id"] == id) {
                            count = data["items"][i]["count"];
                        }
                    }
                }
            });
            return count;
        }
    }, {
        key: "add_to_cart",
        value: function add_to_cart() {
            var id = parseInt(window.location.pathname.split("/")[2]);
            var count = parseInt(document.getElementById("order_count_input").value);
            var count_in_shopping_cart = this.get_count_of_item_from_shopping_cart();
            console.log(count_in_shopping_cart);
            if (count_in_shopping_cart == 0) {
                $.ajax({
                    url: "/shopping_cart/item",
                    type: "POST",
                    data: JSON.stringify({ "count": count, "id": id }),
                    dataType: "json",
                    contentType: "application/json",
                    success: function success(data) {
                        success_swal("加入成功");
                    },
                    error: function error(xhr, status, _error) {
                        if (_error == "UNAUTHORIZED") {
                            error_swal("加入失敗", "請先登入").then(function () {
                                window.location.href = "/login";
                            });
                        }
                    }
                });
            } else {
                $.ajax({
                    url: "/shopping_cart/item",
                    type: "PUT",
                    data: JSON.stringify({ "count": count + count_in_shopping_cart, "id": id }),
                    dataType: "json",
                    contentType: "application/json",
                    success: function success(data) {
                        success_swal("加入成功");
                    },
                    error: function error(xhr, status, _error2) {
                        if (_error2 == "UNAUTHORIZED") {
                            error_swal("加入失敗", "請先登入").then(function () {
                                window.location.href = "/login";
                            });
                        }
                    }
                });
            }
        }
    }, {
        key: "render",
        value: function render() {
            var _this3 = this;

            var _state = this.state,
                image_href = _state.image_href,
                name = _state.name,
                count = _state.count,
                original_price = _state.original_price,
                discount_price = _state.discount_price,
                description = _state.description;

            return React.createElement(
                "div",
                { className: "mt-20 w-full flex flex-col gap-5 top-[8vh] h-fit" },
                React.createElement(
                    "div",
                    { className: "flex flex-row justify-even w-[70%] mx-auto p-5" },
                    React.createElement(
                        "div",
                        { className: "w-full h-[50vh]" },
                        React.createElement(
                            "div",
                            { className: "w-[50vh] h-[50vh] mx-auto p-5 border-2" },
                            React.createElement("img", { className: "w-full h-full object-scale-up", src: image_href })
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "w-full h-[50vh] flex flex-between flex-col gap-5" },
                        React.createElement(
                            "div",
                            { id: "title", className: "h-[40%]" },
                            React.createElement(
                                "p",
                                { className: "md:text-2xl xl:text-4xl pb-2" },
                                " ",
                                name,
                                " "
                            ),
                            React.createElement(
                                "p",
                                { className: "md:text-sm xl:text-base pb-2 text-gray-500" },
                                " \u5269\u9918\u6578\u91CF ",
                                React.createElement(
                                    "span",
                                    { className: "underline text-black" },
                                    count
                                )
                            ),
                            React.createElement(PriceComponent, { original_price: original_price, discount_price: discount_price })
                        ),
                        React.createElement(
                            "div",
                            { id: "function", className: "h-[40%]" },
                            React.createElement(
                                "div",
                                null,
                                React.createElement(
                                    "p",
                                    { className: "py-1" },
                                    "\u6578\u91CF"
                                ),
                                React.createElement(
                                    "div",
                                    { className: "flex flex-row h-full" },
                                    React.createElement(
                                        "button",
                                        { className: "bg-slate-500 w-[50px] md:h-[50%] xl:h-[30%] rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300", onClick: function onClick() {
                                                return _this3.increase_count();
                                            } },
                                        "+"
                                    ),
                                    React.createElement("input", { type: "text", id: "order_count_input", className: "text-center w-[100px] md:h-[50%] xl:h-[30%] border-slate-300 border-2 outline-none", defaultValue: "1" }),
                                    React.createElement(
                                        "button",
                                        { className: "bg-slate-500 w-[50px] md:h-[50%] xl:h-[30%] rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300", onClick: function onClick() {
                                                return _this3.decrease_count();
                                            } },
                                        "-"
                                    )
                                )
                            )
                        ),
                        React.createElement(
                            "div",
                            { id: "button-set", className: "flex flex-row gap-5 h-fit" },
                            React.createElement(
                                "button",
                                { className: "py-2 my-auto w-full h-fit bg-orange-500 rounded-md hover:bg-orange-400 duration-300 text-white font-bold shadow-md  disabled:bg-slate-400 disabled:text-slate-100", onClick: function onClick() {
                                        return _this3.add_to_cart();
                                    } },
                                " \u52A0\u5165\u8CFC\u7269\u8ECA "
                            )
                        )
                    )
                ),
                React.createElement("hr", { className: "w-[70%] mx-auto" }),
                React.createElement(
                    "div",
                    { className: "relative w-[70%] mx-auto text-lg" },
                    this.newline_map_description(description)
                )
            );
        }
    }]);

    return MainPlatform;
}(React.Component);

var App = function (_React$Component3) {
    _inherits(App, _React$Component3);

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