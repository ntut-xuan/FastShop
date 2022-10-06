class NevigationBar extends React.Component {
    constructor(props){
        super(props);
        this.nav_extend_on = this.nav_extend_on.bind(this);
        this.nav_extend_off = this.nav_extend_off.bind(this);
    }
    nav_extend_on(){
        document.getElementById("nav_extend_main").classList.remove("h-0")
        document.getElementById("nav_extend_main").classList.add("h-80")
    }
    nav_extend_off(){
        document.getElementById("nav_extend_main").classList.remove("h-80")
        document.getElementById("nav_extend_main").classList.add("h-0")
    }
    render(){
        let clickable_text = "h-full transition-all duration-200 hover:bg-gray-400 hover:text-white px-5 cursor-pointer"
        return [
            <div className="w-full fixed top-0 left-0 z-20 bg-white">
                <div className="w-[90%] mx-auto h-20 flex flex-row relative left-0 top-0">
                    <div className="w-full h-full gap-10 flex-row flex justify-start">
                        <img className="h-full w-auto py-5" src="/static/image/fastshop.svg"></img>
                        <div className={clickable_text}>
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 首頁 </p>
                        </div>
                        <div className={clickable_text} onMouseOver={this.nav_extend_on} onMouseOut={this.nav_extend_off}>
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 所有商品 </p>
                        </div>
                        <div className={clickable_text}>
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 最新消息 </p>
                        </div>
                        <div className={clickable_text}>
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 聯繫我們 </p>
                        </div>
                    </div>
                    <div className="w-full h-full mx-auto gap-10 flex-row flex justify-end">
                        <div className={clickable_text}>
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 搜尋 </p>
                        </div>
                        <div className={clickable_text}>
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 登入 </p>
                        </div>
                        <div className={clickable_text}>
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 購物車 </p>
                        </div>
                    </div>
                </div>
            </div>,
            <div id="nav_extend" className="w-full fixed top-0 left-0 z-10 bg-white bg-opacity-90 flex flex-col">
                <div id="nav_extend_offset" className="w-[90%] mx-auto h-20 flex flex-row relative left-0 top-0 transition-all duration-500">

                </div>
                <div id="nav_extend_main" className="w-[60%] mx-auto h-0 flex flex-row justify-start gap-5 relative left-0 top-0 transition-all duration-500 overflow-y-hidden" onMouseOver={this.nav_extend_on} onMouseOut={this.nav_extend_off}>
                    <div className="p-5 text-center">
                        <p className="text-2xl p-5"> - 魔法 - </p>
                        <p className="text-lg border-opacity-0 border-black border-b-2 hover:border-opacity-100 cursor-pointer my-3 py-2 duration-500"> 時間回朔 </p>
                        <p className="text-lg border-opacity-0 border-black border-b-2 hover:border-opacity-100 cursor-pointer my-3 py-2 duration-500"> 資訊安全 </p>
                        <p className="text-lg border-opacity-0 border-black border-b-2 hover:border-opacity-100 cursor-pointer my-3 py-2 duration-500"> 地震 </p>
                    </div>
                    <div className="p-5 text-center">
                        <p className="text-2xl p-5"> - 食物 - </p>
                        <p className="text-lg border-opacity-0 border-black border-b-2 hover:border-opacity-100 cursor-pointer my-3 py-2 duration-500"> 咖啡 </p>
                        <p className="text-lg border-opacity-0 border-black border-b-2 hover:border-opacity-100 cursor-pointer my-3 py-2 duration-500"> 卡布奇諾 </p>
                        <p className="text-lg border-opacity-0 border-black border-b-2 hover:border-opacity-100 cursor-pointer my-3 py-2 duration-500"> 拿鐵 </p>
                    </div>
                </div>
            </div>
        ]
    }
}

class HeaderImage extends React.Component {
    render(){
        return (
            <div className="relative w-full h-full bg-[url('/static/image/advertisement.jpg')]">
                <div className="w-full h-full bg-black bg-opacity-50 absolute">
                    <div className="absolute left-[10%] bottom-[30%] border-l-2 border-white p-5">
                        <p className="text-6xl text-white py-3"> FastShop </p>
                        <p className="text-3xl text-white py-3"> Fast, simple, convenient. </p>
                    </div>
                </div>
            </div>
        )
    }
}

class App extends React.Component {
    render(){
        return (
            <div className="">
                <NevigationBar />
                <HeaderImage />
            </div>
        )
    }
}

const root = ReactDOM.createRoot(document.getElementById("app"))
root.render(<App />)
