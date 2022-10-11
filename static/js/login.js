var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var LoginPlatform = function (_React$Component) {
    _inherits(LoginPlatform, _React$Component);

    function LoginPlatform() {
        _classCallCheck(this, LoginPlatform);

        return _possibleConstructorReturn(this, (LoginPlatform.__proto__ || Object.getPrototypeOf(LoginPlatform)).apply(this, arguments));
    }

    _createClass(LoginPlatform, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                { className: "bg-orange-100 w-screen h-screen" },
                React.createElement(
                    "div",
                    { className: "w-[600px] h-fit bg-white p-10 rounded-lg absolute left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] shadow-lg" },
                    React.createElement(
                        "div",
                        { id: "title", className: "pb-10" },
                        React.createElement("img", { className: "w-24 h-auto mx-auto my-2 rounded-full", src: "https://ntut-xuan.github.io/src/image/fastshop.png" }),
                        React.createElement(
                            "p",
                            { className: "text-center text-2xl" },
                            " \u767B\u5165 "
                        )
                    ),
                    React.createElement(
                        "div",
                        { id: "input_group", className: "" },
                        React.createElement("input", { type: "text", className: "w-full p-3 border-2 border-gray-400 text-xs mb-4 outline-none", placeholder: "\u96FB\u5B50\u90F5\u4EF6\u5730\u5740" }),
                        React.createElement("input", { type: "password", className: "w-full p-3 border-2 border-gray-400 text-xs mb-4 outline-none", placeholder: "\u5BC6\u78BC" })
                    ),
                    React.createElement(
                        "div",
                        { id: "forgot_password", className: "" },
                        React.createElement(
                            "p",
                            { className: "text-sm underline underline-offset-2 cursor-pointer" },
                            " \u5FD8\u8A18\u5BC6\u78BC\uFF1F "
                        )
                    ),
                    React.createElement(
                        "div",
                        { id: "button_group", className: "pt-10" },
                        React.createElement(
                            "button",
                            { className: "bg-black text-white w-full p-2 my-2" },
                            " \u767B\u5165 "
                        ),
                        React.createElement(
                            "button",
                            { className: "bg-amber-600 text-white w-full p-2 my-2" },
                            " \u4F7F\u7528 Google \u9032\u884C\u767B\u5165 "
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
                                { href: "/register", className: "text-sm underline underline-offset-2 my-2 cursor-pointer" },
                                " \u9084\u6C92\u6709\u5E33\u865F\u55CE\uFF1F\u8A3B\u518A\u5E33\u865F "
                            )
                        ),
                        React.createElement(
                            "p",
                            { className: "my-2" },
                            React.createElement(
                                "a",
                                { href: "/", className: "text-sm underline underline-offset-2 my-2 cursor-pointer" },
                                " \u8FD4\u56DE\u5546\u5E97 "
                            )
                        )
                    )
                )
            );
        }
    }]);

    return LoginPlatform;
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
                React.createElement(LoginPlatform, null)
            );
        }
    }]);

    return App;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("app"));
root.render(React.createElement(App, null));