class NevigationBar extends React.Component {
    render(){
        return (
            <div className="w-full h-200">
                <div className="w-[90%] mx-auto h-20 flex flex-row p-5">
                    <div className="w-full h-full  gap-10  flex-row flex justify-start">
                        <img className="h-full w-auto" src="/static/image/fastshop.svg"></img>
                        <div className="h-full">
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 首頁 </p>
                        </div>
                        <div className="h-full">
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 所有商品 </p>
                        </div>
                        <div className="h-full">
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 最新消息 </p>
                        </div>
                        <div className="h-full">
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 聯繫我們 </p>
                        </div>
                    </div>
                    <div className="w-full h-full mx-auto gap-10 p-3 flex-row flex justify-end">
                        <div className="h-full">
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 搜尋 </p>
                        </div>
                        <div className="h-full">
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 登入 </p>
                        </div>
                        <div className="h-full">
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"> 購物車 </p>
                        </div>
                    </div>
                </div>
            </div>
        )
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
