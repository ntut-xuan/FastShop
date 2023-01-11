class MainPlatform extends React.Component {
    render(){
        return (
            <div className="w-screen h-fit overflow-y-scroll overflow-x-hidden flex flex-row bg-gray-100">
                <div className="w-[90%] mx-auto h-[80vh] my-[17vh] rounded-md bg-white flex flex-row p-10 gap-5">
                    <div className="w-[80%] h-full">
                        <div className="border-2 h-full p-5 flex flex-col gap-5">
                            <div className="border-2 rounded-md flex flex-row py-5 cursor-pointer hover:bg-slate-100 hover:duration-500">
                                <div className="md:w-[20%] xl:w-[10%] px-5">
                                    <input type="checkbox" className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] w-[2rem] h-[2rem]" />
                                </div>
                                <div className="md:w-[30%] xl:w-[15%] my-auto border-r-2 border-l-2">
                                    <img className="h-[3rem] w-[3rem] mx-auto" src="/static/images/0f4b3e89-4736-4ca1-89fe-0cc06be76b9d"></img>
                                </div>
                                <div className="md:w-[50%] xl:w-full border-r-2 px-5">
                                    <p className="relative text-lg top-[50%] translate-y-[-50%]"> 暮色黑刃 </p>
                                </div>
                                <div className="md:w-[40%] xl:w-[20%] px-5 border-r-2">
                                    <div className="flex flex-row my-auto h-[3rem]">
                                        <button className="bg-slate-500 w-[50px] h-full rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300" onClick={() => this.increase_count()}>+</button>
                                        <input type="text" id="order_count_input" className="text-center w-[100px] h-full border-slate-300 border-2 outline-none" defaultValue="1"></input>
                                        <button className="bg-slate-500 w-[50px] h-full rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300" onClick={() => this.decrease_count()}>-</button>
                                    </div>
                                </div>
                                <div className="w-[20%] px-5">
                                    <div className="relative top-[50%] translate-y-[-50%]">
                                        <p className="text-lg whitespace-nowrap"> 2900 MC </p>
                                        <p className="text-sm font-bold text-gray-500 line-through whitespace-nowrap"> 3100 MC </p>
                                    </div>
                                </div>
                            </div>
                            <div className="border-2 rounded-md flex flex-row py-5 cursor-pointer hover:bg-slate-100 hover:duration-500">
                                <div className="md:w-[20%] xl:w-[10%] px-5">
                                    <input type="checkbox" className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] w-[2rem] h-[2rem]" />
                                </div>
                                <div className="md:w-[30%] xl:w-[15%] my-auto border-r-2 border-l-2">
                                    <img className="h-[3rem] w-[3rem] mx-auto" src="/static/images/19825dda-dd5d-4b86-8308-ce4fad518b55"></img>
                                </div>
                                <div className="md:w-[50%] xl:w-full border-r-2 px-5">
                                    <p className="relative text-lg top-[50%] translate-y-[-50%]"> 水星彎刀 </p>
                                </div>
                                <div className="md:w-[40%] xl:w-[20%] px-5 border-r-2">
                                    <div className="flex flex-row h-[3rem] my-auto">
                                        <button className="bg-slate-500 w-[3rem] h-full rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300" onClick={() => this.increase_count()}>+</button>
                                        <input type="text" id="order_count_input" className="text-center w-[100px] h-full border-slate-300 border-2 outline-none" defaultValue="1"></input>
                                        <button className="bg-slate-500 w-[3rem] h-full rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300" onClick={() => this.decrease_count()}>-</button>
                                    </div>
                                </div>
                                <div className="w-[20%] px-5">
                                    <div className="relative top-[50%] translate-y-[-50%]">
                                        <p className="text-lg  whitespace-nowrap"> 3000 MC </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="w-[20%] h-full flex justify-end flex-col gap-5">
                        <div className="h-fit py-5 flex flex-col gap-5 p-5 border-2">
                            <p className="text-2xl font-bold"> 總金額 </p>
                            <p className="md:text-2xl xl:text-4xl font-bold text-blue-500 font-mono"> 11700 MC </p>
                            <p className="md:text-xs xl:text-base font-mono"> 已折扣 600 MC</p>
                        </div>
                        <div className="h-fit">
                            <button className="w-full p-5 bg-blue-400 text-white rounded-md">確認訂單</button>
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
