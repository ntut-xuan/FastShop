var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var NevigationBar = function (_React$Component) {
    _inherits(NevigationBar, _React$Component);

    function NevigationBar() {
        _classCallCheck(this, NevigationBar);

        return _possibleConstructorReturn(this, (NevigationBar.__proto__ || Object.getPrototypeOf(NevigationBar)).apply(this, arguments));
    }

    _createClass(NevigationBar, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                { className: "w-full h-200" },
                React.createElement(
                    "div",
                    { className: "w-[90%] mx-auto h-20 flex flex-row p-5" },
                    React.createElement(
                        "div",
                        { className: "w-full h-full  gap-10  flex-row flex justify-start" },
                        React.createElement("img", { className: "h-full w-auto", src: "/static/image/fastshop.svg" }),
                        React.createElement(
                            "div",
                            { className: "h-full" },
                            React.createElement(
                                "p",
                                { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                " \u9996\u9801 "
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "h-full" },
                            React.createElement(
                                "p",
                                { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                " \u6240\u6709\u5546\u54C1 "
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "h-full" },
                            React.createElement(
                                "p",
                                { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                " \u6700\u65B0\u6D88\u606F "
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "h-full" },
                            React.createElement(
                                "p",
                                { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                " \u806F\u7E6B\u6211\u5011 "
                            )
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "w-full h-full mx-auto gap-10 p-3 flex-row flex justify-end" },
                        React.createElement(
                            "div",
                            { className: "h-full" },
                            React.createElement(
                                "p",
                                { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                " \u641C\u5C0B "
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "h-full" },
                            React.createElement(
                                "p",
                                { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                " \u767B\u5165 "
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "h-full" },
                            React.createElement(
                                "p",
                                { className: "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" },
                                " \u8CFC\u7269\u8ECA "
                            )
                        )
                    )
                )
            );
        }
    }]);

    return NevigationBar;
}(React.Component);

var HeaderImage = function (_React$Component2) {
    _inherits(HeaderImage, _React$Component2);

    function HeaderImage() {
        _classCallCheck(this, HeaderImage);

        return _possibleConstructorReturn(this, (HeaderImage.__proto__ || Object.getPrototypeOf(HeaderImage)).apply(this, arguments));
    }

    _createClass(HeaderImage, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                { className: "relative w-full h-full bg-[url('/static/image/advertisement.jpg')]" },
                React.createElement(
                    "div",
                    { className: "w-full h-full bg-black bg-opacity-50 absolute" },
                    React.createElement(
                        "div",
                        { className: "absolute left-[10%] bottom-[30%] border-l-2 border-white p-5" },
                        React.createElement(
                            "p",
                            { className: "text-6xl text-white py-3" },
                            " FastShop "
                        ),
                        React.createElement(
                            "p",
                            { className: "text-3xl text-white py-3" },
                            " Fast, simple, convenient. "
                        )
                    )
                )
            );
        }
    }]);

    return HeaderImage;
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
                React.createElement(HeaderImage, null)
            );
        }
    }]);

    return App;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("app"));
root.render(React.createElement(App, null));
