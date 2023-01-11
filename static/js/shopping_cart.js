var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var MainPlatform = function (_React$Component) {
    _inherits(MainPlatform, _React$Component);

    function MainPlatform() {
        _classCallCheck(this, MainPlatform);

        return _possibleConstructorReturn(this, (MainPlatform.__proto__ || Object.getPrototypeOf(MainPlatform)).apply(this, arguments));
    }

    _createClass(MainPlatform, [{
        key: "render",
        value: function render() {
            var _this2 = this;

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
                            React.createElement(
                                "div",
                                { className: "border-2 rounded-md flex flex-row py-5 cursor-pointer hover:bg-slate-100 hover:duration-500" },
                                React.createElement(
                                    "div",
                                    { className: "md:w-[20%] xl:w-[10%] px-5" },
                                    React.createElement("input", { type: "checkbox", className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] w-[2rem] h-[2rem]" })
                                ),
                                React.createElement(
                                    "div",
                                    { className: "md:w-[30%] xl:w-[15%] my-auto border-r-2 border-l-2" },
                                    React.createElement("img", { className: "h-[3rem] w-[3rem] mx-auto", src: "/static/images/0f4b3e89-4736-4ca1-89fe-0cc06be76b9d" })
                                ),
                                React.createElement(
                                    "div",
                                    { className: "md:w-[50%] xl:w-full border-r-2 px-5" },
                                    React.createElement(
                                        "p",
                                        { className: "relative text-lg top-[50%] translate-y-[-50%]" },
                                        " \u66AE\u8272\u9ED1\u5203 "
                                    )
                                ),
                                React.createElement(
                                    "div",
                                    { className: "md:w-[40%] xl:w-[20%] px-5 border-r-2" },
                                    React.createElement(
                                        "div",
                                        { className: "flex flex-row my-auto h-[3rem]" },
                                        React.createElement(
                                            "button",
                                            { className: "bg-slate-500 w-[50px] h-full rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300", onClick: function onClick() {
                                                    return _this2.increase_count();
                                                } },
                                            "+"
                                        ),
                                        React.createElement("input", { type: "text", id: "order_count_input", className: "text-center w-[100px] h-full border-slate-300 border-2 outline-none", defaultValue: "1" }),
                                        React.createElement(
                                            "button",
                                            { className: "bg-slate-500 w-[50px] h-full rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300", onClick: function onClick() {
                                                    return _this2.decrease_count();
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
                                            "p",
                                            { className: "text-lg whitespace-nowrap" },
                                            " 2900 MC "
                                        ),
                                        React.createElement(
                                            "p",
                                            { className: "text-sm font-bold text-gray-500 line-through whitespace-nowrap" },
                                            " 3100 MC "
                                        )
                                    )
                                )
                            ),
                            React.createElement(
                                "div",
                                { className: "border-2 rounded-md flex flex-row py-5 cursor-pointer hover:bg-slate-100 hover:duration-500" },
                                React.createElement(
                                    "div",
                                    { className: "md:w-[20%] xl:w-[10%] px-5" },
                                    React.createElement("input", { type: "checkbox", className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] w-[2rem] h-[2rem]" })
                                ),
                                React.createElement(
                                    "div",
                                    { className: "md:w-[30%] xl:w-[15%] my-auto border-r-2 border-l-2" },
                                    React.createElement("img", { className: "h-[3rem] w-[3rem] mx-auto", src: "/static/images/19825dda-dd5d-4b86-8308-ce4fad518b55" })
                                ),
                                React.createElement(
                                    "div",
                                    { className: "md:w-[50%] xl:w-full border-r-2 px-5" },
                                    React.createElement(
                                        "p",
                                        { className: "relative text-lg top-[50%] translate-y-[-50%]" },
                                        " \u6C34\u661F\u5F4E\u5200 "
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
                                                    return _this2.increase_count();
                                                } },
                                            "+"
                                        ),
                                        React.createElement("input", { type: "text", id: "order_count_input", className: "text-center w-[100px] h-full border-slate-300 border-2 outline-none", defaultValue: "1" }),
                                        React.createElement(
                                            "button",
                                            { className: "bg-slate-500 w-[3rem] h-full rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300", onClick: function onClick() {
                                                    return _this2.decrease_count();
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
                                            "p",
                                            { className: "text-lg  whitespace-nowrap" },
                                            " 3000 MC "
                                        )
                                    )
                                )
                            )
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
                                " 11700 MC "
                            ),
                            React.createElement(
                                "p",
                                { className: "md:text-xs xl:text-base font-mono" },
                                " \u5DF2\u6298\u6263 600 MC"
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "h-fit" },
                            React.createElement(
                                "button",
                                { className: "w-full p-5 bg-blue-400 text-white rounded-md" },
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