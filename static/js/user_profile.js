var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var OrderRow = function (_React$Component) {
    _inherits(OrderRow, _React$Component);

    function OrderRow(props) {
        _classCallCheck(this, OrderRow);

        var _this = _possibleConstructorReturn(this, (OrderRow.__proto__ || Object.getPrototypeOf(OrderRow)).call(this, props));

        _this.state = {
            id: props.id,
            date: props.date,
            avatars: props.avatars,
            status_code: props.status_code
        };
        return _this;
    }

    _createClass(OrderRow, [{
        key: "status_code_to_zhtw",
        value: function status_code_to_zhtw(status_code) {
            if (status_code == "CHECKING") {
                return "確認中";
            } else if (status_code == "OK") {
                return "訂單完成";
            } else if (status_code == "CANCEL") {
                return "訂單取消";
            }
        }
    }, {
        key: "render",
        value: function render() {
            var _state = this.state,
                id = _state.id,
                date = _state.date,
                avatars = _state.avatars,
                status_code = _state.status_code;

            var avatars_object_list = [];
            for (var i = 0; i < avatars.length; i++) {
                avatars_object_list.push(React.createElement("img", { className: "w-16 h-16", src: "/static/images/".concat(avatars[i]) }));
            }
            return React.createElement(
                "div",
                { className: "w-full h-fit border-2 flex flex-row text-center px-6 gap-5 hover:bg-gray-200 hover:duration-300" },
                React.createElement(
                    "div",
                    { className: "w-fit py-5" },
                    React.createElement(
                        "div",
                        { className: "h-full py-5 pr-5 border-r-2" },
                        React.createElement(
                            "p",
                            { className: "text-center my-auto whitespace-nowrap" },
                            " ",
                            id,
                            " "
                        )
                    )
                ),
                React.createElement(
                    "div",
                    { className: "w-fit py-5" },
                    React.createElement(
                        "div",
                        { className: "h-full py-5 pr-5 border-r-2" },
                        React.createElement(
                            "p",
                            { className: "text-center my-auto whitespace-nowrap" },
                            " ",
                            new Date(date * 1000).toLocaleString('zh-tw', { timeZone: 'Asia/Taipei' }),
                            " "
                        )
                    )
                ),
                React.createElement(
                    "div",
                    { className: "w-full py-5" },
                    React.createElement(
                        "div",
                        { className: "h-full pr-5 border-r-2 flex flex-row gap-3" },
                        avatars_object_list
                    )
                ),
                React.createElement(
                    "div",
                    { className: "w-fit py-5" },
                    React.createElement(
                        "div",
                        { className: "h-full py-5 pr-5 border-r-2" },
                        React.createElement(
                            "p",
                            { className: "text-center my-auto whitespace-nowrap" },
                            " ",
                            this.status_code_to_zhtw(status_code),
                            " "
                        )
                    )
                )
            );
        }
    }]);

    return OrderRow;
}(React.Component);

var MainPlatform = function (_React$Component2) {
    _inherits(MainPlatform, _React$Component2);

    function MainPlatform(props) {
        _classCallCheck(this, MainPlatform);

        var _this2 = _possibleConstructorReturn(this, (MainPlatform.__proto__ || Object.getPrototypeOf(MainPlatform)).call(this, props));

        _this2.state = {
            firstname: "",
            lastname: "",
            birthday: "",
            gender: -1,
            email: "",
            orders: undefined,
            order_total: 0,
            order_item_total: 0,
            order_cost_total: 0,
            order_id_to_order_map: undefined,
            item_id_to_item_avatar: undefined
        };
        _this2.order_row_array = _this2.order_row_array.bind(_this2);
        return _this2;
    }

    _createClass(MainPlatform, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var id_price_map = new Map();
            $.ajax({
                url: "/user",
                method: "GET",
                success: function (data) {
                    this.setState({
                        firstname: data["firstname"],
                        lastname: data["lastname"],
                        birthday: data["birthday"],
                        gender: data["gender"],
                        email: data["e-mail"]
                    });
                }.bind(this)
            });
            $.ajax({
                url: "/items",
                methods: "GET",
                success: function (data) {
                    for (var i = 0; i < data.length; i++) {
                        id_price_map.set(data[i]["id"], data[i]["price"]["discount"]);
                    }
                    var item_id_to_item_avatar = new Map();
                    for (var _i = 0; _i < data.length; _i++) {
                        item_id_to_item_avatar.set(data[_i]["id"], data[_i]["avatar"]);
                    }
                    this.setState({ item_id_to_item_avatar: item_id_to_item_avatar });
                }.bind(this)
            });
            $.ajax({
                url: "/orders",
                methods: "GET",
                success: function (data) {
                    var order_total = data["count"];
                    var order_item_total = 0;
                    var order_cost_total = 0;
                    for (var i = 0; i < data["result"].length; i++) {
                        for (var j = 0; j < data["result"][i]["detail"]["items"].length; j++) {
                            order_item_total += data["result"][i]["detail"]["items"][j]["count"];
                            order_cost_total += data["result"][i]["detail"]["items"][j]["count"] * id_price_map.get(data["result"][i]["detail"]["items"][j]["id"]);
                        }
                    }
                    var order_id_to_order_map = new Map();
                    for (var _i2 = 0; _i2 < data["result"].length; _i2++) {
                        order_id_to_order_map.set(data["result"][_i2]["id"], data["result"][_i2]);
                    }
                    this.setState({
                        orders: data["result"],
                        order_total: order_total,
                        order_item_total: order_item_total,
                        order_cost_total: order_cost_total,
                        order_id_to_order_map: order_id_to_order_map
                    });
                }.bind(this)
            });
        }
    }, {
        key: "logout",
        value: function logout() {
            $.ajax({
                url: "/logout",
                method: "POST",
                success: function success(data) {
                    Swal.fire({
                        icon: "success",
                        title: "登出成功",
                        showConfirmButton: false,
                        timer: 1500,
                        didClose: function didClose() {
                            window.location.href = "/";
                        }
                    });
                }
            });
        }
    }, {
        key: "order_of_avatars",
        value: function order_of_avatars(order_id) {
            var avatars = [];
            var _state2 = this.state,
                order_id_to_order_map = _state2.order_id_to_order_map,
                item_id_to_item_avatar = _state2.item_id_to_item_avatar;

            var order = order_id_to_order_map.get(order_id);
            var order_items = order["detail"]["items"];
            for (var i = 0; i < order_items.length; i++) {
                avatars.push(item_id_to_item_avatar.get(order_items[i]["id"]));
            }
            return avatars;
        }
    }, {
        key: "order_row_array",
        value: function order_row_array() {
            var orders = this.state.orders;

            var order_row_array = [];

            if (orders == undefined) {
                return undefined;
            }

            for (var i = 0; i < orders.length; i++) {
                var order_id = orders[i]["id"];
                order_row_array.push(React.createElement(OrderRow, { id: order_id, date: orders[i]["detail"]["date"], avatars: this.order_of_avatars(order_id), status_code: orders[i]["status"] }));
            }
            return order_row_array;
        }
    }, {
        key: "render",
        value: function render() {
            var _this3 = this;

            var _state3 = this.state,
                firstname = _state3.firstname,
                lastname = _state3.lastname,
                birthday = _state3.birthday,
                gender = _state3.gender,
                email = _state3.email,
                order_total = _state3.order_total,
                order_item_total = _state3.order_item_total,
                order_cost_total = _state3.order_cost_total;

            var order_row_object_array = this.order_row_array();
            return React.createElement(
                "div",
                { className: "md:w-[90%] xl:w-[80%] md:h-[80vh] xl:h-[90vh] mx-auto flex flex-row border-2 my-20 rounded-md bg-gray-100" },
                React.createElement(
                    "div",
                    { className: "w-[30%] h-full p-5" },
                    React.createElement(
                        "div",
                        { className: "h-full w-full border-2 bg-white rounded-md flex flex-col xl:p-10 md:p-3" },
                        React.createElement(
                            "div",
                            { className: "mx-auto w-fit h-full p-5 flex flex-col" },
                            React.createElement("img", { className: "w-[60%] h-auto mx-auto rounded-full border-2", src: gender == 0 ? "/static/image/boy.png" : gender == 1 ? "/static/image/girl.png" : "" }),
                            React.createElement(
                                "div",
                                { className: "pt-5" },
                                React.createElement(
                                    "p",
                                    { className: "md:text-xl xl:text-2xl font-bold" },
                                    " ",
                                    firstname,
                                    " ",
                                    lastname,
                                    " "
                                ),
                                React.createElement(
                                    "div",
                                    { className: "pt-5" },
                                    React.createElement(
                                        "p",
                                        { className: "md:text-base xl:text-xl py-2 text-gray-500 font-mono whitespace-nowrap" },
                                        React.createElement("i", { "class": "fa-solid fa-envelope fa-fw" }),
                                        " ",
                                        email,
                                        " "
                                    ),
                                    React.createElement(
                                        "p",
                                        { className: "md:text-base xl:text-xl py-2 text-gray-500 font-mono" },
                                        React.createElement("i", { "class": "fa-solid fa-cake-candles fa-fw" }),
                                        " ",
                                        birthday,
                                        " "
                                    )
                                )
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "h-fit" },
                            React.createElement(
                                "button",
                                { className: "relative p-3 text-center w-full rounded-md bg-orange-200", onClick: function onClick() {
                                        return _this3.logout();
                                    } },
                                " \u767B\u51FA "
                            )
                        )
                    )
                ),
                React.createElement(
                    "div",
                    { className: "w-[70%] h-full py-5 pr-5 flex flex-col gap-5" },
                    React.createElement(
                        "div",
                        { className: "h-fit flex flex-row gap-5" },
                        React.createElement(
                            "div",
                            { className: "flex flex-col border-2 w-full bg-white rounded-md" },
                            React.createElement(
                                "div",
                                { className: "md:text-6xl xl:text-8xl h-fit py-3" },
                                React.createElement(
                                    "p",
                                    { className: "text-center font-bold text-amber-500 px-5" },
                                    order_total
                                )
                            ),
                            React.createElement(
                                "div",
                                { className: "h-fit py-3" },
                                React.createElement(
                                    "p",
                                    { className: "text-center text-xl" },
                                    "\u5DF2\u8CFC\u8CB7\u8A02\u55AE"
                                )
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "flex flex-col border-2 w-full bg-white rounded-md" },
                            React.createElement(
                                "div",
                                { className: "md:text-6xl xl:text-8xl h-fit py-3" },
                                React.createElement(
                                    "p",
                                    { className: "text-center font-bold text-teal-500 px-5" },
                                    order_item_total
                                )
                            ),
                            React.createElement(
                                "div",
                                { className: "h-fit py-3" },
                                React.createElement(
                                    "p",
                                    { className: "text-center text-xl" },
                                    "\u5DF2\u8CFC\u8CB7\u7269\u54C1\u6578\u91CF"
                                )
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "flex flex-col border-2 w-full bg-white rounded-md" },
                            React.createElement(
                                "div",
                                { className: "md:text-6xl xl:text-8xl h-fit py-3" },
                                React.createElement(
                                    "p",
                                    { className: "text-center font-bold px-5 text-blue-500" },
                                    order_cost_total,
                                    "$"
                                )
                            ),
                            React.createElement(
                                "div",
                                { className: "h-fit py-3" },
                                React.createElement(
                                    "p",
                                    { className: "text-center text-xl" },
                                    "\u7D2F\u7A4D\u5DF2\u8CFC\u8CB7\u91D1\u984D"
                                )
                            )
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "border-2 h-[80%] flex flex-col gap-5 p-5 bg-white rounded-md" },
                        React.createElement(
                            "p",
                            { className: "text-center text-xl xl:py-5" },
                            " \u6B77\u53F2\u8A02\u55AE "
                        ),
                        React.createElement(
                            "div",
                            { className: "overflow-y-auto md:h-[20vh] xl:h-[40vh] gap-5 flex flex-col" },
                            order_row_object_array
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