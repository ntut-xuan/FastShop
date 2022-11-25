var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var RegisterPlatform = function (_React$Component) {
    _inherits(RegisterPlatform, _React$Component);

    function RegisterPlatform(props) {
        _classCallCheck(this, RegisterPlatform);

        var _this = _possibleConstructorReturn(this, (RegisterPlatform.__proto__ || Object.getPrototypeOf(RegisterPlatform)).call(this, props));

        _this.state = { firstname: "", lastname: "", gender: -1, birthday: "", email: "", password: "" };
        _this.handleFirstnameChange = _this.handleFirstnameChange.bind(_this);
        _this.handleLastnameChange = _this.handleLastnameChange.bind(_this);
        _this.handleGenderChange = _this.handleGenderChange.bind(_this);
        _this.handleEmailChange = _this.handleEmailChange.bind(_this);
        _this.handlePasswordChange = _this.handlePasswordChange.bind(_this);
        _this.handleSubmit = _this.handleSubmit.bind(_this);
        return _this;
    }

    _createClass(RegisterPlatform, [{
        key: "handleFirstnameChange",
        value: function handleFirstnameChange(event) {
            this.setState({ firstname: event.target.value });
        }
    }, {
        key: "handleLastnameChange",
        value: function handleLastnameChange(event) {
            this.setState({ lastname: event.target.value });
        }
    }, {
        key: "handleGenderChange",
        value: function handleGenderChange(event) {
            this.setState({ gender: event.target.value });
        }
    }, {
        key: "handleEmailChange",
        value: function handleEmailChange(event) {
            this.setState({ email: event.target.value });
        }
    }, {
        key: "handlePasswordChange",
        value: function handlePasswordChange(event) {
            this.setState({ password: event.target.value });
        }
    }, {
        key: "handleSubmit",
        value: function handleSubmit(event) {
            var _state = this.state,
                firstname = _state.firstname,
                lastname = _state.lastname,
                gender = _state.gender,
                birthday = _state.birthday,
                email = _state.email,
                password = _state.password;

            var payload = JSON.stringify({
                "e-mail": email,
                "password": password,
                "firstname": firstname,
                "lastname": lastname,
                "gender": gender,
                "birthday": birthday
            });
            console.log(payload);
            event.preventDefault();
            $.ajax({
                url: "/register",
                type: "POST",
                data: payload,
                dataType: "json",
                contentType: "application/json",
                success: function success(data, status, xhr) {
                    success_swal("註冊成功").then(function () {
                        window.location.href = "/";
                    });
                },
                error: function error(xhr, status, _error) {
                    console.log(_error);
                    if (_error == "FORBIDDEN") {
                        error_swal("註冊失敗", "帳號已存在");
                    } else if (_error === "UNPROCESSABLE ENTITY") {
                        error_swal("註冊失敗", "註冊資料格式錯誤");
                    } else {
                        error_swal("註冊失敗", "註冊 Payload 格式錯誤，請聯繫管理員");
                    }
                }
            });
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            $('[data-toggle="datepicker"]').datepicker({
                onSelect: function (date) {
                    this.setState({ birthday: date });
                }.bind(this),
                dateFormat: 'yy-mm-dd',
                yearRange: "1900:2022",
                changeYear: true,
                changeMonth: true,
                minDate: null,
                maxDate: 0
            });
        }
    }, {
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                { className: "bg-blue-100 w-screen h-screen" },
                React.createElement(
                    "form",
                    { className: "w-[600px] h-fit bg-white p-10 rounded-lg absolute left-[50%] top-[55%] translate-x-[-50%] translate-y-[-50%] shadow-lg", onSubmit: this.handleSubmit },
                    React.createElement(
                        "div",
                        { id: "title", className: "pb-10" },
                        React.createElement(
                            "p",
                            { className: "text-center text-2xl" },
                            " \u8A3B\u518A "
                        )
                    ),
                    React.createElement(
                        "div",
                        { id: "input_group", className: "flex flex-col gap-3" },
                        React.createElement(
                            "div",
                            { className: "flex flex-row gap-3" },
                            React.createElement("input", { type: "text", className: "w-full p-3 border-2 border-gray-400 text-xs outline-none", placeholder: "\u59D3\u6C0F", onChange: this.handleFirstnameChange }),
                            React.createElement("input", { type: "text", className: "w-full p-3 border-2 border-gray-400 text-xs outline-none", placeholder: "\u540D\u7A31", onChange: this.handleLastnameChange })
                        ),
                        React.createElement(
                            "div",
                            { className: "flex flex-row gap-3" },
                            React.createElement(
                                "select",
                                { className: "w-full p-3 border-2 border-gray-400 text-xs outline-none", defaultValue: "\u6027\u5225", onChange: this.handleGenderChange },
                                React.createElement(
                                    "option",
                                    { className: "w-full text-xs", disabled: "disabled" },
                                    "\u6027\u5225"
                                ),
                                React.createElement(
                                    "option",
                                    { className: "w-full text-xs", value: "0" },
                                    "\u7537\u6027"
                                ),
                                React.createElement(
                                    "option",
                                    { className: "w-full text-xs", value: "1" },
                                    "\u5973\u6027"
                                )
                            ),
                            React.createElement("input", { type: "text", className: "w-full p-3 border-2 border-gray-400 text-xs outline-none", placeholder: "\u51FA\u751F\u65E5\u671F", "data-toggle": "datepicker" })
                        ),
                        React.createElement("input", { type: "text", className: "w-full p-3 border-2 border-gray-400 text-xs outline-none", placeholder: "\u96FB\u5B50\u90F5\u4EF6\u5730\u5740", onChange: this.handleEmailChange }),
                        React.createElement("input", { type: "password", className: "w-full p-3 border-2 border-gray-400 text-xs outline-none", placeholder: "\u5BC6\u78BC", onChange: this.handlePasswordChange })
                    ),
                    React.createElement(
                        "div",
                        { id: "declare", className: "py-5" },
                        React.createElement(
                            "p",
                            { className: "text-sm" },
                            "\u4E00\u65E6\u9EDE\u64CA\u8A3B\u518A\uFF0C\u5373\u8868\u793A\u4F60\u540C\u610F FastShop \u7684",
                            React.createElement(
                                "a",
                                { className: "text-sm decoration-black underline underline-offset-2 cursor-pointer" },
                                "\u670D\u52D9\u689D\u6B3E"
                            ),
                            "\uFF0C",
                            React.createElement(
                                "a",
                                { className: "text-sm underline underline-offset-2 cursor-pointer" },
                                "\u96B1\u79C1\u653F\u7B56"
                            ),
                            "\u548C",
                            React.createElement(
                                "a",
                                { className: "text-sm underline underline-offset-2 cursor-pointer" },
                                "\u9000\u6B3E\u653F\u7B56"
                            ),
                            "\u3002"
                        )
                    ),
                    React.createElement(
                        "div",
                        { id: "button_group", className: "" },
                        React.createElement(
                            "button",
                            { className: "bg-black text-white w-full p-2 my-2" },
                            " \u8A3B\u518A "
                        ),
                        React.createElement(
                            "a",
                            { href: "#" },
                            React.createElement(
                                "p",
                                { className: "bg-blue-600 text-white w-full p-2 my-2 text-center" },
                                " \u4F7F\u7528 Google \u9032\u884C\u8A3B\u518A "
                            )
                        )
                    ),
                    React.createElement(
                        "div",
                        { id: "footer_text", className: "text-center pt-10" },
                        React.createElement(
                            "p",
                            { className: "my-2" },
                            React.createElement(
                                "a",
                                { href: "/login", className: "text-sm underline underline-offset-2 cursor-pointer" },
                                " \u5DF2\u7D93\u6709\u5E33\u865F\u4E86\uFF1F\u767B\u5165\u5E33\u865F "
                            )
                        ),
                        React.createElement(
                            "p",
                            { className: "my-2" },
                            React.createElement(
                                "a",
                                { href: "/", className: "text-sm underline underline-offset-2 cursor-pointer" },
                                " \u8FD4\u56DE\u5546\u5E97 "
                            )
                        )
                    )
                )
            );
        }
    }]);

    return RegisterPlatform;
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
                React.createElement(RegisterPlatform, null)
            );
        }
    }]);

    return App;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("app"));
root.render(React.createElement(App, null));