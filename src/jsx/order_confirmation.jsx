class MainPlatform extends React.Component {
    constructor(props){
        super(props)
    }
    render(){
        return (
            <div className="w-screen h-screen">
                <div className="h-[92vh] my-[8vh] w-full flex flex-row overflow-y-hidden">
                    <div className="w-[60%] h-full p-10 flex flex-row justify-end">
                        <div className="h-full w-[60%] flex flex-col gap-10">
                            <div className="flex flex-col gap-5">
                                <p className="text-2xl"> 收件人資訊 </p>
                                <div className="p-5 flex flex-row gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300">
                                    <img className="h-24 w-auto rounded-full border-2" src="/static/image/boy.png"></img>
                                    <div className="p-3 gap-3 flex flex-col">
                                        <p> 黃漢軒 </p>
                                        <p className="font-mono"> sigtunatw@gmail.com </p>
                                    </div>
                                </div>
                                <div className="p-5 flex flex-col gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300">
                                    <div className="flex flex-row w-full">
                                        <p className="w-[20%] text-center my-auto"> 聯絡電話 </p>
                                        <input type="text" className="border-2 w-[80%] p-1 font-mono" placeholder="0923456789"></input>
                                    </div>
                                    <div className="flex flex-row w-full">
                                        <p className="w-[20%] text-center my-auto"> 地址 </p>
                                        <input type="text" className="border-2 w-[80%] p-1" placeholder="臺北市大安區忠孝東路一段 1 號"></input>
                                    </div>
                                </div>
                            </div>
                            <div className="flex flex-col gap-5">
                                <p className="text-2xl"> 訂單備註 </p>
                                <div className="p-5 flex flex-col gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300">
                                    <div className="flex flex-row w-full">
                                        <textarea className="border-2 p-1 w-full h-[10vh] font-mono resize-none rounded-md"></textarea>
                                    </div>
                                </div>
                            </div>
                            <div className="flex flex-col gap-5">
                                <p className="text-2xl"> 付款資訊 </p>
                                <div className="p-5 flex flex-col gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300">
                                    <div className="flex flex-row w-full">
                                        <input type="radio" className="border-2 p-1 w-[20%] font-mono" checked></input>
                                        <label className="w-[80%] my-auto">貨到付款</label>
                                    </div>
                                </div>
                            </div>
                            <button className="w-full p-2 bg-green-500 text-white rounded-md">立即下單</button>
                        </div>
                    </div>
                    <div className="w-[40%] h-full bg-gray-100 p-10">
                        <div className="h-full w-[70%] flex flex-col gap-10">
                            <div className="flex flex-col gap-5">
                                <p className="text-2xl"> 購物車 </p>
                                <div className="p-5 flex flex-row gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300 bg-white">
                                    <img src="/static/images/0f4b3e89-4736-4ca1-89fe-0cc06be76b9d" className="h-16 w-16 rounded-md"></img>
                                    <div className="flex flex-col gap-3 my-auto w-[60%]">
                                        <p> 暮色黑刃 </p>
                                        <p> 數量：3 個</p>
                                    </div>
                                    <div className="h-full">
                                        <p className="my-auto">8700 MC</p>
                                    </div>
                                </div>
                                <div className="p-5 flex flex-row gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300 bg-white">
                                    <img src="/static/images/19825dda-dd5d-4b86-8308-ce4fad518b55" className="h-16 w-16 rounded-md"></img>
                                    <div className="flex flex-col gap-3 my-auto w-[60%]">
                                        <p> 水星彎刀 </p>
                                        <p> 數量：1 個</p>
                                    </div>
                                    <div className="h-full">
                                        <p className="my-auto">3000 MC</p>
                                    </div>
                                </div>
                                <hr className="w-full"></hr>
                                <div className="flex flex-col gap-2">
                                    <div className="flex flex-row w-full px-5">
                                        <p className="w-full">合計</p>
                                        <p className="w-full text-right">11900 MC</p>
                                    </div>
                                    <div className="flex flex-row w-full px-5">
                                        <p className="w-full">運費</p>
                                        <p className="w-full text-right">2000 MC</p>
                                    </div>
                                </div>
                                <hr className="w-full"></hr>
                                <div className="flex flex-col gap-2">
                                    <div className="flex flex-row w-full px-5">
                                        <p className="w-full my-auto">總金額</p>
                                        <p className="w-full text-right text-2xl font-bold">13900 MC</p>
                                    </div>
                                </div>
                            </div>
                        </div>
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
                <MainPlatform />
            </div>
        )
    }
}

const root = ReactDOM.createRoot(document.getElementById("app"))
root.render(<App />)
