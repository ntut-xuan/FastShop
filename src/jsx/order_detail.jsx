class Item extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            avatar: props.avatar,
            item_name: props.item_name,
            count: props.count,
            price: props.price
        }
    }
    render(){
        let {avatar, item_name, count, price} = this.state
        return (
            <div className="p-5 flex flex-row gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300 bg-white">
                <img src={"/static/images/".concat(avatar)} className="h-16 w-16 rounded-md"></img>
                <div className="flex flex-col gap-3 my-auto w-[60%]">
                    <p> {item_name} </p>
                    <p> 數量：{count} 個</p>
                </div>
                <div className="h-full">
                    <p className="my-auto whitespace-nowrap">{count*price} MC</p>
                </div>
            </div>
        )
    }
}

class MainPlatform extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            id: undefined,
            name: undefined,
            email: undefined,
            phone_number: undefined,
            address: undefined,
            note: undefined,
            order_items: undefined,
            delivery_status: undefined,
            order_status: undefined
        }
    }
    fetch_items_list(items){
        let item_id_to_item_map = new Map()
        $.ajax({
            url: "/items",
            type: "GET",
            async: false,
            success: function(data){
                for(let i = 0; i < data.length; i++){
                    item_id_to_item_map.set(data[i]["id"], data[i])
                }
            }
        }).then(() => {
            let result = []
            for(let i = 0; i < items.length; i++){
                let item = item_id_to_item_map.get(items[i]["id"])
                result.push({"item_detail": item, "count": items[i]["count"]})
            }
            this.setState({
                order_items: result,
            })
        })
    }
    componentDidMount(){
        let id = parseInt(window.location.pathname.split("/")[2])
        $.ajax({
            url: "/orders/".concat(id),
            type: "GET",
            async: false,
            success: function(data){
                this.setState({
                    id: data["id"],
                    name: data["detail"]["delivery_info"]["lastname"] + " " + data["detail"]["delivery_info"]["firstname"],
                    email: data["detail"]["delivery_info"]["email"],
                    phone_number: data["detail"]["delivery_info"]["phone_number"],
                    address: data["detail"]["delivery_info"]["address"],
                    note: data["detail"]["note"],
                    delivery_status: data["delivery_status"],
                    order_status: data["status"]
                })
                this.fetch_items_list(data["detail"]["items"])
            }.bind(this)
        })
    }
    get_total_of_order(){
        let {order_items} = this.state
        let total = 0
        for(let i = 0; i < order_items.length; i++){
            total += order_items[i]["count"] * order_items[i]["item_detail"]["price"]["discount"]
        }
        return total
    }
    get_order_item_object_list(){
        let {order_items} = this.state
        let list = []
        for(let i = 0; i < order_items.length; i++){
            list.push(
                <Item avatar={order_items[i]["item_detail"]["avatar"]} item_name={order_items[i]["item_detail"]["name"]} count={order_items[i]["count"]} price={order_items[i]["item_detail"]["price"]["discount"]}></Item>
            )
        }
        return list
    }
    order_status_to_zhtw(status){
        if(status == "CHECKING"){
            return "確認中"
        }
        if(status == "OK"){
            return "訂單完成"
        }
        if(status == "CANCEL"){
            return "訂單取消"
        }
        return ""
    }
    delivery_status_to_zhtw(status){
        if(status == "SKIP"){
            return "訂單不寄送"
        }
        if(status == "PENDING"){
            return "正在準備出貨"
        }
        if(status == "DELIVERING"){
            return "貨物寄送中"
        }
        if(status == "DELIVERED"){
            return "貨物已送達"
        }
        return ""
    }
    render(){
        let {id, name, email, phone_number, address, note, order_items, delivery_status, order_status} = this.state
        if(order_items == undefined){
            return <div></div>
        }
        let total = this.get_total_of_order()
        return (
            <div className="w-screen h-screen">
                <div className="h-[92vh] my-[8vh] w-full flex flex-row overflow-y-hidden">
                    <div className="w-[60%] h-full flex flex-row justify-end p-10">
                        <div className="h-full w-[60%] flex flex-col gap-10">
                            <div className="flex flex-col gap-5">
                                <p className="text-2xl"> 訂單編號 {id} ─ 收件人資訊 </p>
                                <div className="p-5 flex flex-row gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300">
                                    <img className="h-24 w-auto rounded-full border-2" src="/static/image/boy.png"></img>
                                    <div className="p-3 gap-3 flex flex-col">
                                        <p> {name} </p>
                                        <p className="font-mono"> {email} </p>
                                    </div>
                                </div>
                                <div className="p-5 flex flex-col gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300">
                                    <div className="flex flex-row w-full">
                                        <p className="w-[20%] text-center my-auto"> 聯絡電話 </p>
                                        <input id="phone_number" type="text" className="border-2 w-[80%] p-1 font-mono" placeholder={phone_number} readOnly></input>
                                    </div>
                                    <div className="flex flex-row w-full">
                                        <p className="w-[20%] text-center my-auto"> 地址 </p>
                                        <input id="address" type="text" className="border-2 w-[80%] p-1" placeholder={address} readOnly></input>
                                    </div>
                                </div>
                            </div>
                            <div className="flex flex-col gap-5">
                                <p className="text-2xl"> 訂單備註 </p>
                                <div className="p-5 flex flex-col gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300">
                                    <div className="flex flex-row w-full">
                                        <textarea id="note" className="border-2 p-1 w-full h-[10vh] font-mono resize-none rounded-md" placeholder={note} readOnly></textarea>
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
                        </div>
                    </div>
                    <div className="w-[40%] h-full p-10 flex flex-row bg-gray-100">
                        <div className="h-full w-[70%] flex flex-col gap-20">
                            <div className="flex flex-col gap-5">
                                <p className="text-2xl"> 訂單內容 </p>
                                {this.get_order_item_object_list()}
                                <hr className="w-full"></hr>
                                <div className="flex flex-col gap-2">
                                    <div className="flex flex-row w-full px-5">
                                        <p className="w-full">合計</p>
                                        <p className="w-full text-right"> {total} MC</p>
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
                                        <p className="w-full text-right text-2xl font-bold"> {total+2000} MC</p>
                                    </div>
                                </div>
                            </div>
                            <div className="flex flex-col gap-5">
                                <p className="text-2xl"> 訂單狀態 </p>
                                <div className="flex flex-row w-full px-5">
                                    <p className="w-full">訂單處理狀態</p>
                                    <p className="w-full text-right"> {this.order_status_to_zhtw(order_status)}</p>
                                </div>
                                <div className="flex flex-row w-full px-5">
                                    <p className="w-full">運送狀態</p>
                                    <p className="w-full text-right"> {this.delivery_status_to_zhtw(delivery_status)}</p>
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
