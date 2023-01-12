var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Item = function (_React$Component) {
    _inherits(Item, _React$Component);

    function Item(props) {
        _classCallCheck(this, Item);

        var _this = _possibleConstructorReturn(this, (Item.__proto__ || Object.getPrototypeOf(Item)).call(this, props));

        _this.state = {
            id: props.id,
            avatar: props.avatar,
            item_name: props.item_name,
            count: props.count,
            price: props.price,
            refresh_sum: props.refresh_sum,
            item_list: props.item_list
        };
        return _this;
    }

    _createClass(Item, [{
        key: "increase_count",
        value: function increase_count() {
            var id = this.state.id;

            var value = document.getElementById("item_count_".concat(id)).value;
            var int_value = parseInt(value);
            if (isNaN(int_value)) {
                int_value = 0;
            }
            int_value = int_value + 1;
            document.getElementById("item_count_".concat(id)).value = int_value;
            this.update_count(id, int_value);
        }
    }, {
        key: "decrease_count",
        value: function decrease_count() {
            var id = this.state.id;

            var value = document.getElementById("item_count_".concat(id)).value;
            var int_value = parseInt(value);
            if (isNaN(int_value)) {
                int_value = 0;
            }
            int_value = Math.max(int_value - 1, 0);
            document.getElementById("item_count_".concat(id)).value = int_value;
            this.update_count(id, int_value);
            if (int_value == 0) {
                document.getElementById("item_tab_".concat(id)).classList.add("hidden");
            }
        }
    }, {
        key: "update_count",
        value: function update_count(id, count) {
            $.ajax({
                url: "/shopping_cart/item",
                type: "PUT",
                data: JSON.stringify({ "count": count, "id": id }),
                dataType: "json",
                contentType: "application/json",
                success: function success(data) {},
                error: function error(xhr, status, _error) {
                    if (_error == "UNAUTHORIZED") {
                        error_swal("加入失敗", "請先登入").then(function () {
                            window.location.href = "/login";
                        });
                    }
                    if (_error == "FORBIDDEN") {
                        error_swal("物品數量更改失敗");
                    }
                }
            });
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            var refresh_sum = this.state.refresh_sum;

            refresh_sum();
        }
    }, {
        key: "render",
        value: function render() {
            var _this2 = this;

            var _state = this.state,
                id = _state.id,
                avatar = _state.avatar,
                item_name = _state.item_name,
                count = _state.count,
                price = _state.price,
                refresh_sum = _state.refresh_sum;

            return React.createElement(
                "div",
                { id: "item_tab_".concat(id), className: "border-2 rounded-md flex flex-row py-5 cursor-pointer hover:bg-slate-100 hover:duration-500" },
                React.createElement(
                    "div",
                    { className: "md:w-[30%] xl:w-[15%] my-auto border-r-2 border-l-2" },
                    React.createElement("img", { className: "h-[3rem] w-[3rem] mx-auto", src: "/static/images/".concat(avatar) })
                ),
                React.createElement(
                    "div",
                    { className: "md:w-[50%] xl:w-full border-r-2 px-5" },
                    React.createElement(
                        "p",
                        { className: "relative text-lg top-[50%] translate-y-[-50%]" },
                        " ",
                        item_name,
                        " "
                    )
                ),
                React.createElement(
                    "div",
                    { className: "md:w-[40%] xl:w-[20%] px-5 border-r-2" },
                    React.createElement(
                        "div",
                        { className: "flex flex-row h-[3rem] my-auto" },
                        React.createElement(
                            "button",
                            { className: "bg-slate-500 w-[3rem] h-full rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300", onClick: function onClick() {
                                    _this2.increase_count();refresh_sum();
                                } },
                            "+"
                        ),
                        React.createElement("input", { id: "item_count_".concat(id), type: "text", className: "text-center w-[100px] h-full border-slate-300 border-2 outline-none", defaultValue: count }),
                        React.createElement(
                            "button",
                            { className: "bg-slate-500 w-[3rem] h-full rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300", onClick: function onClick() {
                                    _this2.decrease_count();refresh_sum();
                                } },
                            "-"
                        )
                    )
                ),
                React.createElement(
                    "div",
                    { className: "w-[20%] px-5" },
                    React.createElement(
                        "div",
                        { className: "relative top-[50%] translate-y-[-50%]" },
                        React.createElement(
                            "span",
                            { name: "item_price_".concat(id), className: "text-lg  whitespace-nowrap" },
                            " ",
                            price,
                            " "
                        ),
                        React.createElement(
                            "span",
                            { className: "text-lg  whitespace-nowrap" },
                            " MC "
                        )
                    )
                )
            );
        }
    }]);

    return Item;
}(React.Component);

var MainPlatform = function (_React$Component2) {
    _inherits(MainPlatform, _React$Component2);

    function MainPlatform(props) {
        _classCallCheck(this, MainPlatform);

        var _this3 = _possibleConstructorReturn(this, (MainPlatform.__proto__ || Object.getPrototypeOf(MainPlatform)).call(this, props));

        _this3.state = {
            item_list: [],
            total: 0
        };
        _this3.refresh_sum = _this3.refresh_sum.bind(_this3);
        return _this3;
    }

    _createClass(MainPlatform, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var _this4 = this;

            var item_list = this.state.item_list;

            $.ajax({
                url: "/shopping_cart",
                type: "GET",
                async: false,
                success: function success(data) {
                    var _loop = function _loop(i) {
                        var id = data["items"][i]["id"];
                        var count = data["items"][i]["count"];
                        var price = data["items"][i]["price"];
                        $.ajax({
                            url: "/items/".concat(id),
                            type: "GET",
                            async: false,
                            success: function success(item_data) {
                                var avatar = item_data["avatar"];
                                var name = item_data["name"];
                                item_list.push({
                                    "avatar": avatar,
                                    "id": id,
                                    "count": count,
                                    "price": price,
                                    "name": name
                                });
                            }
                        });
                    };

                    for (var i = 0; i < data["count"]; i++) {
                        _loop(i);
                    }
                }
            }).then(function () {
                _this4.setState({ item_list: item_list });
            });
        }
    }, {
        key: "refresh_sum",
        value: function refresh_sum() {
            var item_list = this.state.item_list;

            var sum = 0;
            for (var i = 0; i < item_list.length; i++) {
                count = document.getElementById("item_count_".concat(item_list[i]["id"])).value;
                sum += item_list[i]["price"] * count;
            }
            this.setState({ total: sum });
        }
    }, {
        key: "render",
        value: function render() {
            var _state2 = this.state,
                item_list = _state2.item_list,
                total = _state2.total;

            var item_object_list = [];
            for (var i = 0; i < item_list.length; i++) {
                item_object_list.push(React.createElement(Item, {
                    id: item_list[i]["id"],
                    avatar: item_list[i]["avatar"],
                    count: item_list[i]["count"],
                    item_name: item_list[i]["name"],
                    price: item_list[i]["price"],
                    refresh_sum: this.refresh_sum }));
            }
            return React.createElement(
                "div",
                { className: "w-screen h-fit overflow-y-scroll overflow-x-hidden flex flex-row bg-gray-100" },
                React.createElement(
                    "div",
                    { className: "w-[90%] mx-auto h-[80vh] my-[17vh] rounded-md bg-white flex flex-row p-10 gap-5" },
                    React.createElement(
                        "div",
                        { className: "w-[80%] h-full" },
                        React.createElement(
                            "div",
                            { className: "border-2 h-full p-5 flex flex-col gap-5" },
                            item_object_list
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "w-[20%] h-full flex justify-end flex-col gap-5" },
                        React.createElement(
                            "div",
                            { className: "h-fit py-5 flex flex-col gap-5 p-5 border-2" },
                            React.createElement(
                                "p",
                                { className: "text-2xl font-bold" },
                                " \u7E3D\u91D1\u984D "
                            ),
                            React.createElement(
                                "p",
                                { className: "md:text-2xl xl:text-4xl font-bold text-blue-500 font-mono" },
                                " ",
                                total,
                                " MC "
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "h-fit" },
                            React.createElement(
                                "button",
                                { className: "w-full p-5 bg-blue-400 text-white rounded-md", onClick: function onClick() {
                                        window.location.href = "/order_confirmation";
                                    } },
                                "\u78BA\u8A8D\u8A02\u55AE"
                            )
                        )
                    )
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