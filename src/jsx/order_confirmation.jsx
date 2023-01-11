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
                    <p className="my-auto">{count*price} MC</p>
                </div>
            </div>
        )
    }
}

class MainPlatform extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            item_list: [],
            total: 0,
            firstname: "",
            lastname: "",
            email: ""
        }
        this.submit_order = this.submit_order.bind(this)
    }
    fetch_item_list(){
        let {item_list} = this.state
        $.ajax({
            url: "/shopping_cart",
            type: "GET",
            async: false,
            success: function(data){
                for(let i = 0; i < data["count"]; i++){
                    let id = data["items"][i]["id"]
                    let count = data["items"][i]["count"]
                    let price = data["items"][i]["price"]
                    $.ajax({
                        url: "/items/".concat(id),
                        type: "GET",
                        async: false,
                        success: function(item_data){
                            let avatar = item_data["avatar"]
                            let name = item_data["name"]
                            item_list.push({
                                "avatar": avatar,
                                "id": id,
                                "count": count,
                                "price": price,
                                "name": name
                            })
                        }
                    })
                }
            }
        }).then(() => {
            this.setState({item_list: item_list})
        })
    }
    fetch_user_profile(){
        let firstname = ""
        let lastname = ""
        let email = ""
        $.ajax({
            url: "/user",
            type: "GET",
            async: false,
            success: function(data){
                firstname = data["firstname"]
                lastname = data["lastname"]
                email = data["e-mail"]
            }
        })
        this.setState({firstname: firstname, lastname: lastname, email: email})
    }
    componentDidMount(){
        this.fetch_item_list()
        this.fetch_user_profile()
    }
    submit_order(){
        let {item_list, firstname, lastname, email} = this.state
        let item_list_payload = []
        for(let i = 0; i < item_list.length; i++){
            item_list_payload.push({
                "count": item_list[i]["count"],
                "id": item_list[i]["id"]
            })
        }
        payload = {
            "date": Math.floor(Date.now() / 1000),
            "delivery_info": {
                "address": document.getElementById("address").value,
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "phone_number": document.getElementById("phone_number").value
            },
            "items": item_list_payload,
            "note": document.getElementById("note").value
        }
        $.ajax({
            url: "/orders",
            type: "POST",
            data: JSON.stringify(payload),
            dataType: "json",
            contentType: "application/json",
            success: function(data){
                success_swal("訂單創立成功").then(() => {window.location.href = "/profile"})
            },
        })
    }
    render(){
        let {item_list, firstname, lastname, email} = this.state
        let item_object_list = []
        let name = lastname + " " + firstname
        let total = 0
        for(let i = 0; i < item_list.length; i++){
            item_object_list.push(<Item avatar={item_list[i]["avatar"]} item_name={item_list[i]["name"]} count={item_list[i]["count"]} price={item_list[i]["price"]}></Item>)
            total += item_list[i]["count"] * item_list[i]["price"]
        }
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
                                        <p> {name} </p>
                                        <p className="font-mono"> {email} </p>
                                    </div>
                                </div>
                                <div className="p-5 flex flex-col gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300">
                                    <div className="flex flex-row w-full">
                                        <p className="w-[20%] text-center my-auto"> 聯絡電話 </p>
                                        <input id="phone_number" type="text" className="border-2 w-[80%] p-1 font-mono" placeholder="0923456789"></input>
                                    </div>
                                    <div className="flex flex-row w-full">
                                        <p className="w-[20%] text-center my-auto"> 地址 </p>
                                        <input id="address" type="text" className="border-2 w-[80%] p-1" placeholder="臺北市大安區忠孝東路一段 1 號"></input>
                                    </div>
                                </div>
                            </div>
                            <div className="flex flex-col gap-5">
                                <p className="text-2xl"> 訂單備註 </p>
                                <div className="p-5 flex flex-col gap-5 border-2 shadow-md hover:shadow-xl hover:duration-300">
                                    <div className="flex flex-row w-full">
                                        <textarea id="note" className="border-2 p-1 w-full h-[10vh] font-mono resize-none rounded-md"></textarea>
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
                            <button className="w-full p-2 bg-green-500 text-white rounded-md" onClick={this.submit_order}>立即下單</button>
                        </div>
                    </div>
                    <div className="w-[40%] h-full bg-gray-100 p-10">
                        <div className="h-full w-[70%] flex flex-col gap-10">
                            <div className="flex flex-col gap-5">
                                <p className="text-2xl"> 購物車 </p>
                                {item_object_list}
                                <hr className="w-full"></hr>
                                <div className="flex flex-col gap-2">
                                    <div className="flex flex-row w-full px-5">
                                        <p className="w-full">合計</p>
                                        <p className="w-full text-right">{total} MC</p>
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
                                        <p className="w-full text-right text-2xl font-bold">{total+2000} MC</p>
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
