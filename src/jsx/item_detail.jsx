class MainPlatform extends React.Component {
    constructor(props){
        super(props)
        this.state = {item_name: "Entropy"}
    }
    render(){
        let {item_name} = this.state
        return(
            <div className="mt-20 fixed w-full flex flex-col gap-5 top-[8vh] overflow-y-auto">
                <div className="flex flex-row justify-between w-[70%] h-full mx-auto">
                    <div className="w-full h-fit">
                        <div className="w-[30rem] h-[30rem] bg-slate-400">
                            <img className="w-full h-full object-scale-down" src="https://jamesclear.com/wp-content/uploads/2017/06/entropy.jpg"></img>
                        </div>
                    </div>
                    <div className="w-full">
                        <div id="title">
                            <p className="text-4xl pb-5"> Entropy </p>
                        </div>
                        <div id="price">
                            <p className="text-2xl pb-5 font-serif">
                                <span className="pr-5"> NT$ 43210 </span>
                                <span className="pr-5 font-bold text-gray-400 line-through"> NT$ 48763 </span>
                                <span className="pr-5 font-bold"> -11.49% </span>
                            </p>
                        </div>
                        <div id="function" className="py-16 pb-32">
                            <div>
                                <p className="py-2">數量</p>
                                <div className="flex flex-row">
                                    <button className="bg-slate-500 w-[50px] h-[50px] rounded-sm font-mono text-2xl text-white hover:bg-slate-400 duration-300">+</button>
                                    <input type="text" className="text-center w-[100px] h-[50px] border-slate-300 border-2 outline-none" value="1"></input>
                                    <button className="bg-slate-500 w-[50px] h-[50px] rounded-sm font-mono text-2xl text-white hover:bg-slate-400 duration-300">-</button>
                                </div>
                            </div>
                        </div>
                        <div id="button-set" className="flex gap-5">
                            <button className="py-2 w-full bg-amber-500 rounded-md hover:bg-amber-400 duration-300 text-white font-bold shadow-md"> 直接購買 </button>
                            <button className="py-2 w-full bg-orange-500 rounded-md hover:bg-orange-400 duration-300 text-white font-bold shadow-md"> 加入購物車 </button>
                        </div>
                    </div>
                </div>
                <hr className="w-[70%] mx-auto" />
                <div className="relative w-[70%] mx-auto text-lg">
                    <p>很電的 Entropy :D</p>
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
