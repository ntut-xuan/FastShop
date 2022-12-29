var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var MainPlatform = function (_React$Component) {
    _inherits(MainPlatform, _React$Component);

    function MainPlatform(props) {
        _classCallCheck(this, MainPlatform);

        var _this = _possibleConstructorReturn(this, (MainPlatform.__proto__ || Object.getPrototypeOf(MainPlatform)).call(this, props));

        _this.state = {
            firstname: "",
            lastname: "",
            birthday: "",
            gender: -1,
            email: ""
        };
        return _this;
    }

    _createClass(MainPlatform, [{
        key: "componentDidMount",
        value: function componentDidMount() {
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
        key: "render",
        value: function render() {
            var _this2 = this;

            var _state = this.state,
                firstname = _state.firstname,
                lastname = _state.lastname,
                birthday = _state.birthday,
                gender = _state.gender,
                email = _state.email;

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
                                        return _this2.logout();
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
                                    "9999"
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
                                    "9999"
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
                                    "774653$"
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
                            React.createElement(
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
                                            " 33458762 "
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
                                            " 2022-12-28 16:54:00 "
                                        )
                                    )
                                ),
                                React.createElement(
                                    "div",
                                    { className: "w-full py-5" },
                                    React.createElement(
                                        "div",
                                        { className: "h-full pr-5 border-r-2 flex flex-row gap-3" },
                                        React.createElement("img", { className: "w-16 h-16", src: "/static/images/0ac00df4-9908-42a4-a915-ea1252065a77" }),
                                        React.createElement("img", { className: "w-16 h-16", src: "/static/images/85bc9958-6a0e-4d6a-9a53-cb4ba2b0c3e3" })
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
                                            " \u5DF2\u7D50\u55AE "
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

var App = function (_React$Component2) {
    _inherits(App, _React$Component2);

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