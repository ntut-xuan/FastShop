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
                block_url = "/profile";
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
                            "a",
                            { href: "/" },
                            React.createElement(
                                "div",
                                { className: clickable_text },
                                React.createElement(
                                    "p",
                                    { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                    "\u9996\u9801"
                                )
                            )
                        ),
                        React.createElement(
                            "a",
                            { href: "/items_list" },
                            React.createElement(
                                "div",
                                { className: clickable_text, onMouseOver: this.nav_extend_on, onMouseOut: this.nav_extend_off },
                                React.createElement(
                                    "p",
                                    { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                    "\u6240\u6709\u5546\u54C1"
                                )
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
                                "a",
                                { href: "/cart" },
                                React.createElement(
                                    "p",
                                    { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                    "\u8CFC\u7269\u8ECA"
                                )
                            )
                        )
                    )
                )
            )];
        }
    }]);

    return NevigationBar;
}(React.Component);