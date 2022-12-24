class MainPlatform extends React.Component {
    render(){
        return (
            <div className="mt-20 fixed w-full">
                <div className="w-[80%] h-screen mx-auto flex flex-row gap-5 my-10">
                    <div className="w-[30%]">
                        <p className="w-full text-center p-5 text-2xl"> 類別 </p>
                        <hr />
                        <div className="overflow-y-auto h-[75vh] pt-5">
                            <p className="p-2 text-center"><a href="#"> 資訊安全 </a></p>
                            <p className="p-2 text-center"><a href="#"> 樹學 </a></p>
                            <p className="p-2 text-center"><a href="#"> 數學 </a></p>
                            <p className="p-2 text-center"><a href="#"> 玄學 </a></p>
                        </div>
                    </div>
                    <div className="w-[70%]">
                        <p className="w-full text-center p-5 text-2xl"> 所有商品 </p>
                        <hr />
                        <div className="w-full overflow-y-auto h-[75vh] grid grid-cols-3">
                            <div className="p-5 w-fit h-fit">
                                <div id="items_image" className="w-[30vh] h-[30vh] bg-slate-400 mx-auto">
                                    <a href="/item_list/1">
                                        <img className="w-full h-full object-scale-down" src="https://jamesclear.com/wp-content/uploads/2017/06/entropy.jpg"></img>
                                    </a>
                                </div>
                                <a href="/item_list/1"><p className="text-center p-2"> Entropy </p></a>
                                <p className="text-center"> 4.87 MC </p>
                                <p className="text-center text-sm"> <span className="line-through">5 MC</span> <span className="font-bold">-2.6%</span> </p>
                            </div>
                            <div className="p-5 w-fit h-fit">
                                <div id="items_image" className="w-[30vh] h-[30vh] bg-slate-400 mx-auto">
                                    <a href="/item_list/1">
                                        <img className="w-full h-full object-scale-down" src="https://jamesclear.com/wp-content/uploads/2017/06/entropy.jpg"></img>
                                    </a>
                                </div>
                                <a href="/item_list/1"><p className="text-center p-2"> Entropy </p></a>
                                <p className="text-center"> 4.87 MC </p>
                                <p className="text-center text-sm"> <span className="line-through">5 MC</span> <span className="font-bold">-2.6%</span> </p>
                            </div>
                            <div className="p-5 w-fit h-fit">
                                <div id="items_image" className="w-[30vh] h-[30vh] bg-slate-400 mx-auto">
                                    <a href="/item_list/1">
                                        <img className="w-full h-full object-scale-down" src="https://jamesclear.com/wp-content/uploads/2017/06/entropy.jpg"></img>
                                    </a>
                                </div>
                                <a href="/item_list/1"><p className="text-center p-2"> Entropy </p></a>
                                <p className="text-center"> 4.87 MC </p>
                                <p className="text-center text-sm"> <span className="line-through">5 MC</span> <span className="font-bold">-2.6%</span> </p>
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
