class OrderRow extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            id: props.id,
            date: props.date,
            avatars: props.avatars,
            status_code: props.status_code
        }
    }
    status_code_to_zhtw(status_code){
        if(status_code == "CHECKING"){
            return "確認中"
        }else if(status_code == "OK"){
            return "訂單完成"
        }else if(status_code == "CANCEL"){
            return "訂單取消"
        }
    }
    render(){
        let {id, date, avatars, status_code} = this.state
        let avatars_object_list = []
        for(let i = 0; i < avatars.length; i++){
            avatars_object_list.push(<img className="w-16 h-16" src={"/static/images/".concat(avatars[i])}></img>)
        }
        return (
            <a href={"/order_detail/".concat(id)}>
                <div className="w-full h-fit border-2 flex flex-row text-center px-6 gap-5 hover:bg-gray-200 hover:duration-300">
                    <div className="w-fit py-5">
                        <div className="h-full py-5 pr-5 border-r-2">
                            <p className="text-center my-auto whitespace-nowrap"> {id} </p>
                        </div>
                    </div>
                    <div className="w-fit py-5">
                        <div className="h-full py-5 pr-5 border-r-2">
                            <p className="text-center my-auto whitespace-nowrap"> {new Date(date*1000).toLocaleString('zh-tw', { timeZone: 'Asia/Taipei' })} </p>
                        </div>
                    </div>
                    <div className="w-full py-5">
                        <div className="h-full pr-5 border-r-2 flex flex-row gap-3">
                            {avatars_object_list}
                        </div>
                    </div>
                    <div className="w-fit py-5">
                        <div className="h-full py-5 pr-5 border-r-2">
                            <p className="text-center my-auto whitespace-nowrap"> {this.status_code_to_zhtw(status_code)} </p>
                        </div>
                    </div>
                </div>
            </a>
        )
    }
}

class MainPlatform extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            firstname: "",
            lastname: "",
            birthday: "",
            gender: -1,
            email: "",
            orders: undefined,
            order_total: 0,
            order_item_total: 0,
            order_cost_total: 0,
            order_id_to_order_map: undefined,
            item_id_to_item_avatar: undefined,
        }
        this.order_row_array = this.order_row_array.bind(this)
    }
    componentDidMount(){
        let id_price_map = new Map();
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
        $.ajax({
            url: "/items",
            methods: "GET",
            success: function(data){
                for(let i = 0; i < data.length; i++){
                    id_price_map.set(data[i]["id"], data[i]["price"]["discount"])
                }
                let item_id_to_item_avatar = new Map()
                for(let i = 0; i < data.length; i++){
                    item_id_to_item_avatar.set(data[i]["id"], data[i]["avatar"])
                }
                this.setState({item_id_to_item_avatar: item_id_to_item_avatar})
            }.bind(this)
        })
        $.ajax({
            url: "/orders",
            methods: "GET",
            success: function(data){
                let order_total = data["count"]
                let order_item_total = 0
                let order_cost_total = 0
                for(let i = 0; i < data["result"].length; i++){
                    for(let j = 0; j < data["result"][i]["detail"]["items"].length; j++){
                        order_item_total += data["result"][i]["detail"]["items"][j]["count"]
                        order_cost_total += data["result"][i]["detail"]["items"][j]["count"] * id_price_map.get(data["result"][i]["detail"]["items"][j]["id"])
                    }
                }
                let order_id_to_order_map = new Map()
                for(let i = 0; i < data["result"].length; i++){
                    order_id_to_order_map.set(data["result"][i]["id"], data["result"][i])
                }
                this.setState({
                    orders: data["result"],
                    order_total: order_total,
                    order_item_total: order_item_total,
                    order_cost_total: order_cost_total,
                    order_id_to_order_map: order_id_to_order_map
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
    order_of_avatars(order_id){
        let avatars = []
        let {order_id_to_order_map, item_id_to_item_avatar} = this.state
        let order = order_id_to_order_map.get(order_id)
        let order_items = order["detail"]["items"]
        for(let i = 0; i < order_items.length; i++){
            avatars.push(item_id_to_item_avatar.get(order_items[i]["id"]))
        }
        return avatars
    }
    order_row_array(){
        let {orders} = this.state
        let order_row_array = []

        if(orders == undefined){
            return undefined
        }

        for(let i = 0; i < orders.length; i++){
            let order_id = orders[i]["id"]
            order_row_array.push(
                <OrderRow id={order_id} date={orders[i]["detail"]["date"]} avatars={this.order_of_avatars(order_id)} status_code={orders[i]["status"]} ></OrderRow>
            )
        }
        return order_row_array
    }
    render(){
        let {firstname, lastname, birthday, gender, email, order_total, order_item_total, order_cost_total} = this.state
        let order_row_object_array = this.order_row_array()
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
                                <p className="text-center font-bold text-amber-500 px-5">{order_total}</p>
                            </div>
                            <div className="h-fit py-3">
                                <p className="text-center text-xl">已購買訂單</p>
                            </div>
                        </div>
                        <div className="flex flex-col border-2 w-full bg-white rounded-md">
                            <div className="md:text-6xl xl:text-8xl h-fit py-3">
                                <p className="text-center font-bold text-teal-500 px-5">{order_item_total}</p>
                            </div>
                            <div className="h-fit py-3">
                                <p className="text-center text-xl">已購買物品數量</p>
                            </div>
                        </div>
                        <div className="flex flex-col border-2 w-full bg-white rounded-md">
                            <div className="md:text-6xl xl:text-8xl h-fit py-3">
                                <p className="text-center font-bold px-5 text-blue-500">{order_cost_total}$</p>
                            </div>
                            <div className="h-fit py-3">
                                <p className="text-center text-xl">累積已購買金額</p>
                            </div>
                        </div>
                    </div>
                    <div className="border-2 h-[80%] flex flex-col gap-5 p-5 bg-white rounded-md">
                        <p className="text-center text-xl xl:py-5"> 歷史訂單 </p>
                        <div className="overflow-y-auto md:h-[20vh] xl:h-[40vh] gap-5 flex flex-col">
                            {order_row_object_array}
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
