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
                        { className: "my-auto" },
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
            item_list: [],
            total: 0,
            firstname: "",
            lastname: "",
            email: ""
        };
        _this2.submit_order = _this2.submit_order.bind(_this2);
        return _this2;
    }

    _createClass(MainPlatform, [{
        key: "fetch_item_list",
        value: function fetch_item_list() {
            var _this3 = this;

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
                _this3.setState({ item_list: item_list });
            });
        }
    }, {
        key: "fetch_user_profile",
        value: function fetch_user_profile() {
            var firstname = "";
            var lastname = "";
            var email = "";
            $.ajax({
                url: "/user",
                type: "GET",
                async: false,
                success: function success(data) {
                    firstname = data["firstname"];
                    lastname = data["lastname"];
                    email = data["e-mail"];
                }
            });
            this.setState({ firstname: firstname, lastname: lastname, email: email });
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            this.fetch_item_list();
            this.fetch_user_profile();
        }
    }, {
        key: "submit_order",
        value: function submit_order() {
            var _state2 = this.state,
                item_list = _state2.item_list,
                firstname = _state2.firstname,
                lastname = _state2.lastname,
                email = _state2.email;

            var item_list_payload = [];
            for (var i = 0; i < item_list.length; i++) {
                item_list_payload.push({
                    "count": item_list[i]["count"],
                    "id": item_list[i]["id"]
                });
            }
            payload = {
                "date": Math.floor(Date.now() / 1000),
                "delivery_info": {
                    "address": document.getElementById("address").value,
                    "email": email,
                    "firstname": firstname,
                    "lastname": lastname,
                    "phone_number": document.getElementById("phone_number").value
                },
                "items": item_list_payload,
                "note": document.getElementById("note").value
            };
            $.ajax({
                url: "/orders",
                type: "POST",
                data: JSON.stringify(payload),
                dataType: "json",
                contentType: "application/json",
                success: function success(data) {
                    success_swal("訂單創立成功").then(function () {
                        window.location.href = "/profile";
                    });
                }
            });
        }
    }, {
        key: "render",
        value: function render() {
            var _state3 = this.state,
                item_list = _state3.item_list,
                firstname = _state3.firstname,
                lastname = _state3.lastname,
                email = _state3.email;

            var item_object_list = [];
            var name = lastname + " " + firstname;
            var total = 0;
            for (var i = 0; i < item_list.length; i++) {
                item_object_list.push(React.createElement(Item, { avatar: item_list[i]["avatar"], item_name: item_list[i]["name"], count: item_list[i]["count"], price: item_list[i]["price"] }));
                total += item_list[i]["count"] * item_list[i]["price"];
            }
            return React.createElement(
                "div",
                { className: "w-screen h-screen" },
                React.createElement(
                    "div",
                    { className: "h-[92vh] my-[8vh] w-full flex flex-row overflow-y-hidden" },
                    React.createElement(
                        "div",
                        { className: "w-[60%] h-full p-10 flex flex-row justify-end" },
                        React.createElement(
                            "div",
                            { className: "h-full w-[60%] flex flex-col gap-10" },
                            React.createElement(
                                "div",
                                { className: "flex flex-col gap-5" },
                                React.createElement(
                                    "p",
                                    { className: "text-2xl" },
                                    " \u6536\u4EF6\u4EBA\u8CC7\u8A0A "
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
                                        React.createElement("input", { id: "phone_number", type: "text", className: "border-2 w-[80%] p-1 font-mono", placeholder: "0923456789" })
                                    ),
                                    React.createElement(
                                        "div",
                                        { className: "flex flex-row w-full" },
                                        React.createElement(
                                            "p",
                                            { className: "w-[20%] text-center my-auto" },
                                            " \u5730\u5740 "
                                        ),
                                        React.createElement("input", { id: "address", type: "text", className: "border-2 w-[80%] p-1", placeholder: "\u81FA\u5317\u5E02\u5927\u5B89\u5340\u5FE0\u5B5D\u6771\u8DEF\u4E00\u6BB5 1 \u865F" })
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
                                        React.createElement("textarea", { id: "note", className: "border-2 p-1 w-full h-[10vh] font-mono resize-none rounded-md" })
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
                            ),
                            React.createElement(
                                "button",
                                { className: "w-full p-2 bg-green-500 text-white rounded-md", onClick: this.submit_order },
                                "\u7ACB\u5373\u4E0B\u55AE"
                            )
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "w-[40%] h-full bg-gray-100 p-10" },
                        React.createElement(
                            "div",
                            { className: "h-full w-[70%] flex flex-col gap-10" },
                            React.createElement(
                                "div",
                                { className: "flex flex-col gap-5" },
                                React.createElement(
                                    "p",
                                    { className: "text-2xl" },
                                    " \u8CFC\u7269\u8ECA "
                                ),
                                item_object_list,
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
                                            total + 2000,
                                            " MC"
                                        )
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