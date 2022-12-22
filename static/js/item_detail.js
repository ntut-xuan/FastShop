var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var MainPlatform = function (_React$Component) {
    _inherits(MainPlatform, _React$Component);

    function MainPlatform(props) {
        _classCallCheck(this, MainPlatform);

        var _this = _possibleConstructorReturn(this, (MainPlatform.__proto__ || Object.getPrototypeOf(MainPlatform)).call(this, props));

        _this.state = { item_name: "Entropy" };
        return _this;
    }

    _createClass(MainPlatform, [{
        key: "render",
        value: function render() {
            var item_name = this.state.item_name;

            return React.createElement(
                "div",
                { className: "mt-20 fixed w-full flex flex-col gap-5 top-32" },
                React.createElement(
                    "div",
                    { className: "flex flex-row justify-between w-[70%] h-full mx-auto top-28" },
                    React.createElement(
                        "div",
                        { className: "w-full h-fit" },
                        React.createElement(
                            "div",
                            { className: "w-[30rem] h-[30rem] bg-slate-400" },
                            React.createElement("img", { className: "w-full h-full object-scale-down", src: "https://jamesclear.com/wp-content/uploads/2017/06/entropy.jpg" })
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "w-full" },
                        React.createElement(
                            "div",
                            { id: "title" },
                            React.createElement(
                                "p",
                                { className: "text-4xl pb-5" },
                                " Entropy "
                            )
                        ),
                        React.createElement(
                            "div",
                            { id: "price" },
                            React.createElement(
                                "p",
                                { className: "text-2xl pb-5 font-serif" },
                                React.createElement(
                                    "span",
                                    { className: "pr-5" },
                                    " NT$ 43210 "
                                ),
                                React.createElement(
                                    "span",
                                    { className: "pr-5 font-bold text-gray-400 line-through" },
                                    " NT$ 48763 "
                                ),
                                React.createElement(
                                    "span",
                                    { className: "pr-5 font-bold" },
                                    " -11.49% "
                                )
                            )
                        ),
                        React.createElement(
                            "div",
                            { id: "function", className: "py-16 pb-32" },
                            React.createElement(
                                "div",
                                null,
                                React.createElement(
                                    "p",
                                    { className: "py-2" },
                                    "\u6578\u91CF"
                                ),
                                React.createElement(
                                    "div",
                                    { className: "flex flex-row" },
                                    React.createElement(
                                        "button",
                                        { className: "bg-slate-500 w-[50px] h-[50px] rounded-sm font-mono text-2xl text-white hover:bg-slate-400 duration-300" },
                                        "+"
                                    ),
                                    React.createElement("input", { type: "text", className: "text-center w-[100px] h-[50px] border-slate-300 border-2 outline-none", value: "1" }),
                                    React.createElement(
                                        "button",
                                        { className: "bg-slate-500 w-[50px] h-[50px] rounded-sm font-mono text-2xl text-white hover:bg-slate-400 duration-300" },
                                        "-"
                                    )
                                )
                            )
                        ),
                        React.createElement(
                            "div",
                            { id: "button-set", className: "flex gap-5" },
                            React.createElement(
                                "button",
                                { className: "py-2 w-full bg-amber-500 rounded-md hover:bg-amber-400 duration-300 text-white font-bold shadow-md" },
                                " \u76F4\u63A5\u8CFC\u8CB7 "
                            ),
                            React.createElement(
                                "button",
                                { className: "py-2 w-full bg-orange-500 rounded-md hover:bg-orange-400 duration-300 text-white font-bold shadow-md" },
                                " \u52A0\u5165\u8CFC\u7269\u8ECA "
                            )
                        )
                    )
                ),
                React.createElement("hr", { className: "w-[70%] mx-auto" }),
                React.createElement(
                    "div",
                    { className: "relative w-[70%] mx-auto text-lg" },
                    React.createElement(
                        "p",
                        null,
                        "\u5F88\u96FB\u7684 Entropy :D"
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