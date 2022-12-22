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
            return React.createElement(
                "div",
                { className: "mt-20 fixed w-full" },
                React.createElement(
                    "div",
                    { className: "w-[80%] h-screen mx-auto flex flex-row gap-5 my-10" },
                    React.createElement(
                        "div",
                        { className: "w-[30%]" },
                        React.createElement(
                            "p",
                            { className: "w-full text-center p-5 text-2xl" },
                            " \u985E\u5225 "
                        ),
                        React.createElement("hr", null),
                        React.createElement(
                            "div",
                            { className: "overflow-y-auto h-[75vh] pt-5" },
                            React.createElement(
                                "p",
                                { className: "p-2 text-center" },
                                React.createElement(
                                    "a",
                                    { href: "#" },
                                    " \u8CC7\u8A0A\u5B89\u5168 "
                                )
                            ),
                            React.createElement(
                                "p",
                                { className: "p-2 text-center" },
                                React.createElement(
                                    "a",
                                    { href: "#" },
                                    " \u6A39\u5B78 "
                                )
                            ),
                            React.createElement(
                                "p",
                                { className: "p-2 text-center" },
                                React.createElement(
                                    "a",
                                    { href: "#" },
                                    " \u6578\u5B78 "
                                )
                            ),
                            React.createElement(
                                "p",
                                { className: "p-2 text-center" },
                                React.createElement(
                                    "a",
                                    { href: "#" },
                                    " \u7384\u5B78 "
                                )
                            )
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "w-[70%]" },
                        React.createElement(
                            "p",
                            { className: "w-full text-center p-5 text-2xl" },
                            " \u6240\u6709\u5546\u54C1 "
                        ),
                        React.createElement("hr", null),
                        React.createElement(
                            "div",
                            { className: "w-full overflow-y-auto h-[75vh] grid grid-cols-3" },
                            React.createElement(
                                "div",
                                { className: "p-5 w-fit h-fit" },
                                React.createElement(
                                    "div",
                                    { id: "items_image", className: "w-[30vh] h-[30vh] bg-slate-400 mx-auto" },
                                    React.createElement(
                                        "a",
                                        { href: "/item_list/1" },
                                        React.createElement("img", { className: "w-full h-full object-scale-down", src: "https://jamesclear.com/wp-content/uploads/2017/06/entropy.jpg" })
                                    )
                                ),
                                React.createElement(
                                    "a",
                                    { href: "/item_list/1" },
                                    React.createElement(
                                        "p",
                                        { className: "text-center p-2" },
                                        " Entropy "
                                    )
                                ),
                                React.createElement(
                                    "p",
                                    { className: "text-center" },
                                    " 4.87 MC "
                                ),
                                React.createElement(
                                    "p",
                                    { className: "text-center text-sm" },
                                    " ",
                                    React.createElement(
                                        "span",
                                        { className: "line-through" },
                                        "5 MC"
                                    ),
                                    " ",
                                    React.createElement(
                                        "span",
                                        { className: "font-bold" },
                                        "-2.6%"
                                    ),
                                    " "
                                )
                            ),
                            React.createElement(
                                "div",
                                { className: "p-5 w-fit h-fit" },
                                React.createElement(
                                    "div",
                                    { id: "items_image", className: "w-[30vh] h-[30vh] bg-slate-400 mx-auto" },
                                    React.createElement(
                                        "a",
                                        { href: "/item_list/1" },
                                        React.createElement("img", { className: "w-full h-full object-scale-down", src: "https://jamesclear.com/wp-content/uploads/2017/06/entropy.jpg" })
                                    )
                                ),
                                React.createElement(
                                    "a",
                                    { href: "/item_list/1" },
                                    React.createElement(
                                        "p",
                                        { className: "text-center p-2" },
                                        " Entropy "
                                    )
                                ),
                                React.createElement(
                                    "p",
                                    { className: "text-center" },
                                    " 4.87 MC "
                                ),
                                React.createElement(
                                    "p",
                                    { className: "text-center text-sm" },
                                    " ",
                                    React.createElement(
                                        "span",
                                        { className: "line-through" },
                                        "5 MC"
                                    ),
                                    " ",
                                    React.createElement(
                                        "span",
                                        { className: "font-bold" },
                                        "-2.6%"
                                    ),
                                    " "
                                )
                            ),
                            React.createElement(
                                "div",
                                { className: "p-5 w-fit h-fit" },
                                React.createElement(
                                    "div",
                                    { id: "items_image", className: "w-[30vh] h-[30vh] bg-slate-400 mx-auto" },
                                    React.createElement(
                                        "a",
                                        { href: "/item_list/1" },
                                        React.createElement("img", { className: "w-full h-full object-scale-down", src: "https://jamesclear.com/wp-content/uploads/2017/06/entropy.jpg" })
                                    )
                                ),
                                React.createElement(
                                    "a",
                                    { href: "/item_list/1" },
                                    React.createElement(
                                        "p",
                                        { className: "text-center p-2" },
                                        " Entropy "
                                    )
                                ),
                                React.createElement(
                                    "p",
                                    { className: "text-center" },
                                    " 4.87 MC "
                                ),
                                React.createElement(
                                    "p",
                                    { className: "text-center text-sm" },
                                    " ",
                                    React.createElement(
                                        "span",
                                        { className: "line-through" },
                                        "5 MC"
                                    ),
                                    " ",
                                    React.createElement(
                                        "span",
                                        { className: "font-bold" },
                                        "-2.6%"
                                    ),
                                    " "
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