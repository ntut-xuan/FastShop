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
            avatar: props.avatar,
            item_name: props.item_name,
            count: props.count,
            price: props.price
        };
        return _this;
    }

    _createClass(Item, [{
        key: "render",
        value: function render() {
            var _state = this.state,
                avatar = _state.avatar,
                item_name = _state.item_name,
                count = _state.count,
                price = _state.price;

            return React.createElement(
                "div",
                { className: "p-5 flex flex-row gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300 bg-white" },
                React.createElement("img", { src: "/static/images/".concat(avatar), className: "h-16 w-16 rounded-md" }),
                React.createElement(
                    "div",
                    { className: "flex flex-col gap-3 my-auto w-[60%]" },
                    React.createElement(
                        "p",
                        null,
                        " ",
                        item_name,
                        " "
                    ),
                    React.createElement(
                        "p",
                        null,
                        " \u6578\u91CF\uFF1A",
                        count,
                        " \u500B"
                    )
                ),
                React.createElement(
                    "div",
                    { className: "h-full" },
                    React.createElement(
                        "p",
                        { className: "my-auto whitespace-nowrap" },
                        count * price,
                        " MC"
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

        var _this2 = _possibleConstructorReturn(this, (MainPlatform.__proto__ || Object.getPrototypeOf(MainPlatform)).call(this, props));

        _this2.state = {
            id: undefined,
            name: undefined,
            email: undefined,
            phone_number: undefined,
            address: undefined,
            note: undefined,
            order_items: undefined,
            delivery_status: undefined,
            order_status: undefined
        };
        return _this2;
    }

    _createClass(MainPlatform, [{
        key: "fetch_items_list",
        value: function fetch_items_list(items) {
            var _this3 = this;

            var item_id_to_item_map = new Map();
            $.ajax({
                url: "/items",
                type: "GET",
                async: false,
                success: function success(data) {
                    for (var i = 0; i < data.length; i++) {
                        item_id_to_item_map.set(data[i]["id"], data[i]);
                    }
                }
            }).then(function () {
                var result = [];
                for (var i = 0; i < items.length; i++) {
                    var item = item_id_to_item_map.get(items[i]["id"]);
                    result.push({ "item_detail": item, "count": items[i]["count"] });
                }
                _this3.setState({
                    order_items: result
                });
            });
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            var id = parseInt(window.location.pathname.split("/")[2]);
            $.ajax({
                url: "/orders/".concat(id),
                type: "GET",
                async: false,
                success: function (data) {
                    this.setState({
                        id: data["id"],
                        name: data["detail"]["delivery_info"]["lastname"] + " " + data["detail"]["delivery_info"]["firstname"],
                        email: data["detail"]["delivery_info"]["email"],
                        phone_number: data["detail"]["delivery_info"]["phone_number"],
                        address: data["detail"]["delivery_info"]["address"],
                        note: data["detail"]["note"],
                        delivery_status: data["delivery_status"],
                        order_status: data["status"]
                    });
                    this.fetch_items_list(data["detail"]["items"]);
                }.bind(this)
            });
        }
    }, {
        key: "get_total_of_order",
        value: function get_total_of_order() {
            var order_items = this.state.order_items;

            var total = 0;
            for (var i = 0; i < order_items.length; i++) {
                total += order_items[i]["count"] * order_items[i]["item_detail"]["price"]["discount"];
            }
            return total;
        }
    }, {
        key: "get_order_item_object_list",
        value: function get_order_item_object_list() {
            var order_items = this.state.order_items;

            var list = [];
            for (var i = 0; i < order_items.length; i++) {
                list.push(React.createElement(Item, { avatar: order_items[i]["item_detail"]["avatar"], item_name: order_items[i]["item_detail"]["name"], count: order_items[i]["count"], price: order_items[i]["item_detail"]["price"]["discount"] }));
            }
            return list;
        }
    }, {
        key: "order_status_to_zhtw",
        value: function order_status_to_zhtw(status) {
            if (status == "CHECKING") {
                return "確認中";
            }
            if (status == "OK") {
                return "訂單完成";
            }
            if (status == "CANCEL") {
                return "訂單取消";
            }
            return "";
        }
    }, {
        key: "delivery_status_to_zhtw",
        value: function delivery_status_to_zhtw(status) {
            if (status == "SKIP") {
                return "訂單不寄送";
            }
            if (status == "PENDING") {
                return "正在準備出貨";
            }
            if (status == "DELIVERING") {
                return "貨物寄送中";
            }
            if (status == "DELIVERED") {
                return "貨物已送達";
            }
            return "";
        }
    }, {
        key: "render",
        value: function render() {
            var _state2 = this.state,
                id = _state2.id,
                name = _state2.name,
                email = _state2.email,
                phone_number = _state2.phone_number,
                address = _state2.address,
                note = _state2.note,
                order_items = _state2.order_items,
                delivery_status = _state2.delivery_status,
                order_status = _state2.order_status;

            if (order_items == undefined) {
                return React.createElement("div", null);
            }
            var total = this.get_total_of_order();
            return React.createElement(
                "div",
                { className: "w-screen h-screen" },
                React.createElement(
                    "div",
                    { className: "h-[92vh] my-[8vh] w-full flex flex-row overflow-y-hidden" },
                    React.createElement(
                        "div",
                        { className: "w-[60%] h-full flex flex-row justify-end p-10" },
                        React.createElement(
                            "div",
                            { className: "h-full w-[60%] flex flex-col gap-10" },
                            React.createElement(
                                "div",
                                { className: "flex flex-col gap-5" },
                                React.createElement(
                                    "p",
                                    { className: "text-2xl" },
                                    " \u8A02\u55AE\u7DE8\u865F ",
                                    id,
                                    " \u2500 \u6536\u4EF6\u4EBA\u8CC7\u8A0A "
                                ),
                                React.createElement(
                                    "div",
                                    { className: "p-5 flex flex-row gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300" },
                                    React.createElement("img", { className: "h-24 w-auto rounded-full border-2", src: "/static/image/boy.png" }),
                                    React.createElement(
                                        "div",
                                        { className: "p-3 gap-3 flex flex-col" },
                                        React.createElement(
                                            "p",
                                            null,
                                            " ",
                                            name,
                                            " "
                                        ),
                                        React.createElement(
                                            "p",
                                            { className: "font-mono" },
                                            " ",
                                            email,
                                            " "
                                        )
                                    )
                                ),
                                React.createElement(
                                    "div",
                                    { className: "p-5 flex flex-col gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300" },
                                    React.createElement(
                                        "div",
                                        { className: "flex flex-row w-full" },
                                        React.createElement(
                                            "p",
                                            { className: "w-[20%] text-center my-auto" },
                                            " \u806F\u7D61\u96FB\u8A71 "
                                        ),
                                        React.createElement("input", { id: "phone_number", type: "text", className: "border-2 w-[80%] p-1 font-mono", placeholder: phone_number, readOnly: true })
                                    ),
                                    React.createElement(
                                        "div",
                                        { className: "flex flex-row w-full" },
                                        React.createElement(
                                            "p",
                                            { className: "w-[20%] text-center my-auto" },
                                            " \u5730\u5740 "
                                        ),
                                        React.createElement("input", { id: "address", type: "text", className: "border-2 w-[80%] p-1", placeholder: address, readOnly: true })
                                    )
                                )
                            ),
                            React.createElement(
                                "div",
                                { className: "flex flex-col gap-5" },
                                React.createElement(
                                    "p",
                                    { className: "text-2xl" },
                                    " \u8A02\u55AE\u5099\u8A3B "
                                ),
                                React.createElement(
                                    "div",
                                    { className: "p-5 flex flex-col gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300" },
                                    React.createElement(
                                        "div",
                                        { className: "flex flex-row w-full" },
                                        React.createElement("textarea", { id: "note", className: "border-2 p-1 w-full h-[10vh] font-mono resize-none rounded-md", placeholder: note, readOnly: true })
                                    )
                                )
                            ),
                            React.createElement(
                                "div",
                                { className: "flex flex-col gap-5" },
                                React.createElement(
                                    "p",
                                    { className: "text-2xl" },
                                    " \u4ED8\u6B3E\u8CC7\u8A0A "
                                ),
                                React.createElement(
                                    "div",
                                    { className: "p-5 flex flex-col gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300" },
                                    React.createElement(
                                        "div",
                                        { className: "flex flex-row w-full" },
                                        React.createElement("input", { type: "radio", className: "border-2 p-1 w-[20%] font-mono", checked: true }),
                                        React.createElement(
                                            "label",
                                            { className: "w-[80%] my-auto" },
                                            "\u8CA8\u5230\u4ED8\u6B3E"
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "w-[40%] h-full p-10 flex flex-row bg-gray-100" },
                        React.createElement(
                            "div",
                            { className: "h-full w-[70%] flex flex-col gap-20" },
                            React.createElement(
                                "div",
                                { className: "flex flex-col gap-5" },
                                React.createElement(
                                    "p",
                                    { className: "text-2xl" },
                                    " \u8A02\u55AE\u5167\u5BB9 "
                                ),
                                this.get_order_item_object_list(),
                                React.createElement("hr", { className: "w-full" }),
                                React.createElement(
                                    "div",
                                    { className: "flex flex-col gap-2" },
                                    React.createElement(
                                        "div",
                                        { className: "flex flex-row w-full px-5" },
                                        React.createElement(
                                            "p",
                                            { className: "w-full" },
                                            "\u5408\u8A08"
                                        ),
                                        React.createElement(
                                            "p",
                                            { className: "w-full text-right" },
                                            " ",
                                            total,
                                            " MC"
                                        )
                                    ),
                                    React.createElement(
                                        "div",
                                        { className: "flex flex-row w-full px-5" },
                                        React.createElement(
                                            "p",
                                            { className: "w-full" },
                                            "\u904B\u8CBB"
                                        ),
                                        React.createElement(
                                            "p",
                                            { className: "w-full text-right" },
                                            "2000 MC"
                                        )
                                    )
                                ),
                                React.createElement("hr", { className: "w-full" }),
                                React.createElement(
                                    "div",
                                    { className: "flex flex-col gap-2" },
                                    React.createElement(
                                        "div",
                                        { className: "flex flex-row w-full px-5" },
                                        React.createElement(
                                            "p",
                                            { className: "w-full my-auto" },
                                            "\u7E3D\u91D1\u984D"
                                        ),
                                        React.createElement(
                                            "p",
                                            { className: "w-full text-right text-2xl font-bold" },
                                            " ",
                                            total + 2000,
                                            " MC"
                                        )
                                    )
                                )
                            ),
                            React.createElement(
                                "div",
                                { className: "flex flex-col gap-5" },
                                React.createElement(
                                    "p",
                                    { className: "text-2xl" },
                                    " \u8A02\u55AE\u72C0\u614B "
                                ),
                                React.createElement(
                                    "div",
                                    { className: "flex flex-row w-full px-5" },
                                    React.createElement(
                                        "p",
                                        { className: "w-full" },
                                        "\u8A02\u55AE\u8655\u7406\u72C0\u614B"
                                    ),
                                    React.createElement(
                                        "p",
                                        { className: "w-full text-right" },
                                        " ",
                                        this.order_status_to_zhtw(order_status)
                                    )
                                ),
                                React.createElement(
                                    "div",
                                    { className: "flex flex-row w-full px-5" },
                                    React.createElement(
                                        "p",
                                        { className: "w-full" },
                                        "\u904B\u9001\u72C0\u614B"
                                    ),
                                    React.createElement(
                                        "p",
                                        { className: "w-full text-right" },
                                        " ",
                                        this.delivery_status_to_zhtw(delivery_status)
                                    )
                                )
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