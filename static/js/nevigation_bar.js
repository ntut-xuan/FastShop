var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var clickable_text = "h-full transition-all duration-200 hover:bg-gray-400 hover:text-white px-5 cursor-pointer";

var AuthenticationComponent = function (_React$Component) {
    _inherits(AuthenticationComponent, _React$Component);

    function AuthenticationComponent(props) {
        _classCallCheck(this, AuthenticationComponent);

        return _possibleConstructorReturn(this, (AuthenticationComponent.__proto__ || Object.getPrototypeOf(AuthenticationComponent)).call(this, props));
    }

    _createClass(AuthenticationComponent, [{
        key: "render",
        value: function render() {
            var block_style = "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]";
            var block_text = "";
            var block_url = "";
            if (this.props.login == false) {
                block_text = "登入";
                block_url = "/login";
            } else {
                block_text = this.props.username;
                block_url = "#";
            }
            return React.createElement(
                "a",
                { href: block_url },
                React.createElement(
                    "div",
                    { className: clickable_text },
                    React.createElement(
                        "p",
                        { className: block_style },
                        block_text
                    )
                )
            );
        }
    }]);

    return AuthenticationComponent;
}(React.Component);

var NevigationBar = function (_React$Component2) {
    _inherits(NevigationBar, _React$Component2);

    function NevigationBar(props) {
        _classCallCheck(this, NevigationBar);

        var _this2 = _possibleConstructorReturn(this, (NevigationBar.__proto__ || Object.getPrototypeOf(NevigationBar)).call(this, props));

        _this2.state = { login: false, username: null };
        _this2.nav_extend_on = _this2.nav_extend_on.bind(_this2);
        _this2.nav_extend_off = _this2.nav_extend_off.bind(_this2);
        _this2.check_jwt_verify = _this2.check_jwt_verify.bind(_this2);
        return _this2;
    }

    _createClass(NevigationBar, [{
        key: "nav_extend_on",
        value: function nav_extend_on() {
            document.getElementById("nav_extend_main").classList.remove("h-0");
            document.getElementById("nav_extend_main").classList.add("h-80");
        }
    }, {
        key: "nav_extend_off",
        value: function nav_extend_off() {
            document.getElementById("nav_extend_main").classList.remove("h-80");
            document.getElementById("nav_extend_main").classList.add("h-0");
        }
    }, {
        key: "check_jwt_verify",
        value: function check_jwt_verify() {
            $.ajax({
                url: "/verify_jwt",
                type: "POST",
                success: function (data, status, xhr) {
                    this.setState({ login: true, username: data["data"]["firstname"] + " " + data["data"]["lastname"] });
                }.bind(this)
            });
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            this.check_jwt_verify();
        }
    }, {
        key: "render",
        value: function render() {
            var _state = this.state,
                username = _state.username,
                login = _state.login;

            return [React.createElement(
                "div",
                { className: "w-full fixed top-0 left-0 z-20 bg-white" },
                React.createElement(
                    "div",
                    { className: "w-[90%] mx-auto h-20 flex flex-row relative left-0 top-0" },
                    React.createElement(
                        "div",
                        { className: "w-full h-full gap-5 flex-row flex justify-start text-sm text-center" },
                        React.createElement("img", { className: "h-full w-auto py-5", src: "/static/image/fastshop.svg" }),
                        React.createElement(
                            "div",
                            { className: clickable_text },
                            React.createElement(
                                "p",
                                { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                "\u9996\u9801"
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: clickable_text, onMouseOver: this.nav_extend_on, onMouseOut: this.nav_extend_off },
                            React.createElement(
                                "p",
                                { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                "\u6240\u6709\u5546\u54C1"
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: clickable_text },
                            React.createElement(
                                "p",
                                { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                "\u6700\u65B0\u6D88\u606F"
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: clickable_text },
                            React.createElement(
                                "p",
                                { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                "\u806F\u7E6B\u6211\u5011"
                            )
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "w-[50%] h-full mx-auto gap-5 flex-row flex justify-end text-sm text-center" },
                        React.createElement(
                            "div",
                            { className: clickable_text },
                            React.createElement(
                                "p",
                                { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                "\u641C\u5C0B"
                            )
                        ),
                        React.createElement(AuthenticationComponent, { username: username, login: login }),
                        React.createElement(
                            "div",
                            { className: clickable_text },
                            React.createElement(
                                "p",
                                { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                "\u8CFC\u7269\u8ECA"
                            )
                        )
                    )
                )
            ), React.createElement(
                "div",
                { id: "nav_extend", className: "w-full fixed top-0 left-0 z-10 bg-white bg-opacity-90 flex flex-col" },
                React.createElement("div", { id: "nav_extend_offset", className: "w-[90%] mx-auto h-20 flex flex-row relative left-0 top-0 transition-all duration-500" }),
                React.createElement(
                    "div",
                    { id: "nav_extend_main", className: "w-[60%] mx-auto h-0 flex flex-row justify-start gap-5 relative left-0 top-0 transition-all duration-500 overflow-y-hidden", onMouseOver: this.nav_extend_on, onMouseOut: this.nav_extend_off },
                    React.createElement(
                        "div",
                        { className: "p-5 text-center" },
                        React.createElement(
                            "p",
                            { className: "text-2xl p-5" },
                            " - \u9B54\u6CD5 - "
                        ),
                        React.createElement(
                            "p",
                            { className: "text-lg border-opacity-0 border-black border-b-2 hover:border-opacity-100 cursor-pointer my-3 py-2 duration-500" },
                            " \u6642\u9593\u56DE\u6714 "
                        ),
                        React.createElement(
                            "p",
                            { className: "text-lg border-opacity-0 border-black border-b-2 hover:border-opacity-100 cursor-pointer my-3 py-2 duration-500" },
                            " \u8CC7\u8A0A\u5B89\u5168 "
                        ),
                        React.createElement(
                            "p",
                            { className: "text-lg border-opacity-0 border-black border-b-2 hover:border-opacity-100 cursor-pointer my-3 py-2 duration-500" },
                            " \u5730\u9707 "
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "p-5 text-center" },
                        React.createElement(
                            "p",
                            { className: "text-2xl p-5" },
                            " - \u98DF\u7269 - "
                        ),
                        React.createElement(
                            "p",
                            { className: "text-lg border-opacity-0 border-black border-b-2 hover:border-opacity-100 cursor-pointer my-3 py-2 duration-500" },
                            " \u5496\u5561 "
                        ),
                        React.createElement(
                            "p",
                            { className: "text-lg border-opacity-0 border-black border-b-2 hover:border-opacity-100 cursor-pointer my-3 py-2 duration-500" },
                            " \u5361\u5E03\u5947\u8AFE "
                        ),
                        React.createElement(
                            "p",
                            { className: "text-lg border-opacity-0 border-black border-b-2 hover:border-opacity-100 cursor-pointer my-3 py-2 duration-500" },
                            " \u62FF\u9435 "
                        )
                    )
                )
            )];
        }
    }]);

    return NevigationBar;
}(React.Component);