class MainPlatform extends React.Component {
    render(){
        return (
            <div className="mt-20 fixed w-full">
                <div className="w-[80%] h-screen mx-auto flex flex-row gap-5 my-10">
                    <div className="w-[30%]">
                        <p className="w-full text-center p-5 text-2xl"> 選項 </p>
                        <hr />
                        <div className="flex flex-col justify-start mt-8 gap-20 h-[75vh]">
                            <div className="w-[60%] mx-auto" id="option-group-1">
                                <p className="w-full text-center p-5 text-2xl"> 排列方式 </p>
                                <select className="w-full text-center p-2 border-2">
                                    <option> 按照字母順序 A-Z </option>
                                    <option> 按照字母順序 Z-A </option>
                                    <option> 價格, 由高到低 </option>
                                    <option> 價格, 由低到高 </option>
                                    <option> 日期, 由新到舊 </option>
                                    <option> 日期, 由舊到新 </option>
                                </select>
                            </div>
                            <div className="w-[60%] mx-auto" id="option-group-2">
                                <p className="w-full text-center p-5 text-2xl"> 類別 </p>
                                <div>
                                    <p className="p-2 text-center"><a href="#"> 資訊安全 </a></p>
                                    <p className="p-2 text-center"><a href="#"> 樹學 </a></p>
                                    <p className="p-2 text-center"><a href="#"> 數學 </a></p>
                                    <p className="p-2 text-center"><a href="#"> 玄學 </a></p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="w-[70%]">
                        <p className="w-full text-center p-5 text-2xl"> 所有商品 </p>
                        <hr />
                        <div className="w-full overflow-y-auto h-[75vh] grid grid-cols-3 p-10 gap-10">
                            <div className="p-5 w-fit h-fit">
                                <div id="items_image" className="w-72 h-72 bg-slate-400 mx-auto">
                                    <img className="w-full h-full object-scale-down" src="https://jamesclear.com/wp-content/uploads/2017/06/entropy.jpg"></img>
                                </div>
                                <p className="text-center p-2"> Entropy </p>
                                <p className="text-center"> 4.87 MC </p>
                                <p className="text-center text-sm"> <span className="line-through">5 MC</span> <span className="font-bold">-2.6%</span> </p>
                            </div>
                            <div className="p-5 w-fit h-fit">
                                <div id="items_image" className="w-72 h-72 bg-slate-400 mx-auto">
                                    <img className="w-full h-full object-scale-down" src="https://jamesclear.com/wp-content/uploads/2017/06/entropy.jpg"></img>
                                </div>
                                <p className="text-center p-2"> Entropy </p>
                                <p className="text-center"> 4.87 MC </p>
                                <p className="text-center text-sm"> <span className="line-through">5 MC</span> <span className="font-bold">-2.6%</span> </p>
                            </div>
                            <div className="p-5 w-fit h-fit">
                                <div id="items_image" className="w-72 h-72 bg-slate-400 mx-auto">
                                    <img className="w-full h-full object-scale-down" src="https://jamesclear.com/wp-content/uploads/2017/06/entropy.jpg"></img>
                                </div>
                                <p className="text-center p-2"> Entropy </p>
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
