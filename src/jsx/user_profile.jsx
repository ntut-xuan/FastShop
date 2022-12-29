class MainPlatform extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            firstname: "",
            lastname: "",
            birthday: "",
            gender: -1,
            email: ""
        }
    }
    componentDidMount(){
        $.ajax({
            url: "/user",
            method: "GET",
            success: function(data){
                this.setState({
                    firstname: data["firstname"],
                    lastname: data["lastname"],
                    birthday: data["birthday"],
                    gender: data["gender"],
                    email: data["e-mail"]
                })
            }.bind(this)
        })
    }
    logout(){
        $.ajax({
            url: "/logout",
            method: "POST",
            success: function(data){
                Swal.fire({
                    icon: "success",
                    title: "登出成功",
                    showConfirmButton: false,
                    timer: 1500,
                    didClose: () => {
                        window.location.href = "/"
                    }
                })
            }
        })
    }
    render(){
        let {firstname, lastname, birthday, gender, email} = this.state
        return (
            <div className="md:w-[90%] xl:w-[80%] md:h-[80vh] xl:h-[90vh] mx-auto flex flex-row border-2 my-20 rounded-md bg-gray-100">
                <div className="w-[30%] h-full p-5">
                    <div className="h-full w-full border-2 bg-white rounded-md flex flex-col xl:p-10 md:p-3">
                        <div className="mx-auto w-fit h-full p-5 flex flex-col">
                            <img className="w-[60%] h-auto mx-auto rounded-full border-2" src={gender == 0 ? "/static/image/boy.png" : gender == 1 ? "/static/image/girl.png" : ""}></img>
                            <div className="pt-5">
                                <p className="md:text-xl xl:text-2xl font-bold"> {firstname} {lastname} </p>
                                <div className="pt-5">
                                    <p className="md:text-base xl:text-xl py-2 text-gray-500 font-mono whitespace-nowrap"><i class="fa-solid fa-envelope fa-fw"></i> {email} </p>
                                    <p className="md:text-base xl:text-xl py-2 text-gray-500 font-mono"><i class="fa-solid fa-cake-candles fa-fw"></i> {birthday} </p>
                                </div>
                            </div>
                        </div>
                        <div className="h-fit">
                            <button className="relative p-3 text-center w-full rounded-md bg-orange-200" onClick={() => this.logout()}> 登出 </button>
                        </div>
                    </div>
                </div>
                <div className="w-[70%] h-full py-5 pr-5 flex flex-col gap-5">
                    <div className="h-fit flex flex-row gap-5">
                        <div className="flex flex-col border-2 w-full bg-white rounded-md">
                            <div className="md:text-6xl xl:text-8xl h-fit py-3">
                                <p className="text-center font-bold text-amber-500 px-5">9999</p>
                            </div>
                            <div className="h-fit py-3">
                                <p className="text-center text-xl">已購買訂單</p>
                            </div>
                        </div>
                        <div className="flex flex-col border-2 w-full bg-white rounded-md">
                            <div className="md:text-6xl xl:text-8xl h-fit py-3">
                                <p className="text-center font-bold text-teal-500 px-5">9999</p>
                            </div>
                            <div className="h-fit py-3">
                                <p className="text-center text-xl">已購買物品數量</p>
                            </div>
                        </div>
                        <div className="flex flex-col border-2 w-full bg-white rounded-md">
                            <div className="md:text-6xl xl:text-8xl h-fit py-3">
                                <p className="text-center font-bold px-5 text-blue-500">774653$</p>
                            </div>
                            <div className="h-fit py-3">
                                <p className="text-center text-xl">累積已購買金額</p>
                            </div>
                        </div>
                    </div>
                    <div className="border-2 h-[80%] flex flex-col gap-5 p-5 bg-white rounded-md">
                        <p className="text-center text-xl xl:py-5"> 歷史訂單 </p>
                        <div className="overflow-y-auto md:h-[20vh] xl:h-[40vh] gap-5 flex flex-col">
                            <div className="w-full h-fit border-2 flex flex-row text-center px-6 gap-5 hover:bg-gray-200 hover:duration-300">
                                <div className="w-fit py-5">
                                    <div className="h-full py-5 pr-5 border-r-2">
                                        <p className="text-center my-auto whitespace-nowrap"> 33458762 </p>
                                    </div>
                                </div>
                                <div className="w-fit py-5">
                                    <div className="h-full py-5 pr-5 border-r-2">
                                        <p className="text-center my-auto whitespace-nowrap"> 2022-12-28 16:54:00 </p>
                                    </div>
                                </div>
                                <div className="w-full py-5">
                                    <div className="h-full pr-5 border-r-2 flex flex-row gap-3">
                                        <img className="w-16 h-16" src="/static/images/0ac00df4-9908-42a4-a915-ea1252065a77"></img>
                                        <img className="w-16 h-16" src="/static/images/85bc9958-6a0e-4d6a-9a53-cb4ba2b0c3e3"></img>
                                    </div>
                                </div>
                                <div className="w-fit py-5">
                                    <div className="h-full py-5 pr-5 border-r-2">
                                        <p className="text-center my-auto whitespace-nowrap"> 已結單 </p>
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
