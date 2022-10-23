var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var HeaderImage = function (_React$Component) {
    _inherits(HeaderImage, _React$Component);

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
                React.createElement(HeaderImage, null)
            );
        }
    }]);

    return App;
}(React.Component);

var root = ReactDOM.createRoot(document.getElementById("app"));
root.render(React.createElement(App, null));