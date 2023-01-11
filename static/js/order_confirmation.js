var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var MainPlatform = function (_React$Component) {
    _inherits(MainPlatform, _React$Component);

    function MainPlatform(props) {
        _classCallCheck(this, MainPlatform);

        return _possibleConstructorReturn(this, (MainPlatform.__proto__ || Object.getPrototypeOf(MainPlatform)).call(this, props));
    }

    _createClass(MainPlatform, [{
        key: "render",
        value: function render() {
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
                                            " \u9EC3\u6F22\u8ED2 "
                                        ),
                                        React.createElement(
                                            "p",
                                            { className: "font-mono" },
                                            " sigtunatw@gmail.com "
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
                                        React.createElement("input", { type: "text", className: "border-2 w-[80%] p-1 font-mono", placeholder: "0923456789" })
                                    ),
                                    React.createElement(
                                        "div",
                                        { className: "flex flex-row w-full" },
                                        React.createElement(
                                            "p",
                                            { className: "w-[20%] text-center my-auto" },
                                            " \u5730\u5740 "
                                        ),
                                        React.createElement("input", { type: "text", className: "border-2 w-[80%] p-1", placeholder: "\u81FA\u5317\u5E02\u5927\u5B89\u5340\u5FE0\u5B5D\u6771\u8DEF\u4E00\u6BB5 1 \u865F" })
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
                                        React.createElement("textarea", { className: "border-2 p-1 w-full h-[10vh] font-mono resize-none rounded-md" })
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
                                { className: "w-full p-2 bg-green-500 text-white rounded-md" },
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
                                React.createElement(
                                    "div",
                                    { className: "p-5 flex flex-row gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300 bg-white" },
                                    React.createElement("img", { src: "/static/images/0f4b3e89-4736-4ca1-89fe-0cc06be76b9d", className: "h-16 w-16 rounded-md" }),
                                    React.createElement(
                                        "div",
                                        { className: "flex flex-col gap-3 my-auto w-[60%]" },
                                        React.createElement(
                                            "p",
                                            null,
                                            " \u66AE\u8272\u9ED1\u5203 "
                                        ),
                                        React.createElement(
                                            "p",
                                            null,
                                            " \u6578\u91CF\uFF1A3 \u500B"
                                        )
                                    ),
                                    React.createElement(
                                        "div",
                                        { className: "h-full" },
                                        React.createElement(
                                            "p",
                                            { className: "my-auto" },
                                            "8700 MC"
                                        )
                                    )
                                ),
                                React.createElement(
                                    "div",
                                    { className: "p-5 flex flex-row gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300 bg-white" },
                                    React.createElement("img", { src: "/static/images/19825dda-dd5d-4b86-8308-ce4fad518b55", className: "h-16 w-16 rounded-md" }),
                                    React.createElement(
                                        "div",
                                        { className: "flex flex-col gap-3 my-auto w-[60%]" },
                                        React.createElement(
                                            "p",
                                            null,
                                            " \u6C34\u661F\u5F4E\u5200 "
                                        ),
                                        React.createElement(
                                            "p",
                                            null,
                                            " \u6578\u91CF\uFF1A1 \u500B"
                                        )
                                    ),
                                    React.createElement(
                                        "div",
                                        { className: "h-full" },
                                        React.createElement(
                                            "p",
                                            { className: "my-auto" },
                                            "3000 MC"
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
                                            { className: "w-full" },
                                            "\u5408\u8A08"
                                        ),
                                        React.createElement(
                                            "p",
                                            { className: "w-full text-right" },
                                            "11900 MC"
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
                                            "13900 MC"
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