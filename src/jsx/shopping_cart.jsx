class Item extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            id: props.id,
            avatar: props.avatar,
            item_name: props.item_name,
            count: props.count,
            price: props.price,
            refresh_sum: props.refresh_sum,
            item_list: props.item_list
        }
    }
    increase_count(){
        let {id} = this.state
        let value = document.getElementById("item_count_".concat(id)).value
        let int_value = parseInt(value)
        if(isNaN(int_value)){
            int_value = 0;
        }
        int_value = int_value + 1
        document.getElementById("item_count_".concat(id)).value = int_value
        this.update_count(id, int_value)
    }
    decrease_count(){
        let {id} = this.state
        let value = document.getElementById("item_count_".concat(id)).value
        let int_value = parseInt(value)
        if(isNaN(int_value)){
            int_value = 0;
        }
        int_value = Math.max(int_value - 1, 0)
        document.getElementById("item_count_".concat(id)).value = int_value;
        this.update_count(id, int_value)
        if(int_value == 0){
            document.getElementById("item_tab_".concat(id)).classList.add("hidden")
        }
    }
    update_count(id, count){
        $.ajax({
            url: "/shopping_cart/item",
            type: "PUT",
            data: JSON.stringify({"count": count, "id": id}),
            dataType: "json",
            contentType: "application/json",
            success: function(data){},
            error: function(xhr, status, error){
                if(error == "UNAUTHORIZED"){
                    error_swal("加入失敗", "請先登入").then(() => {window.location.href = "/login"});
                }
                if(error == "FORBIDDEN"){
                    error_swal("物品數量更改失敗");
                }
            }
        })
    }
    componentDidMount(){
        let {refresh_sum} = this.state
        refresh_sum()
    }
    render(){
        let {id, avatar, item_name, count, price, refresh_sum} = this.state
        return (
            <div id={"item_tab_".concat(id)} className="border-2 rounded-md flex flex-row py-5 cursor-pointer hover:bg-slate-100 hover:duration-500">
                <div className="md:w-[30%] xl:w-[15%] my-auto border-r-2 border-l-2">
                    <img className="h-[3rem] w-[3rem] mx-auto" src={"/static/images/".concat(avatar)}></img>
                </div>
                <div className="md:w-[50%] xl:w-full border-r-2 px-5">
                    <p className="relative text-lg top-[50%] translate-y-[-50%]"> {item_name} </p>
                </div>
                <div className="md:w-[40%] xl:w-[20%] px-5 border-r-2">
                    <div className="flex flex-row h-[3rem] my-auto">
                        <button className="bg-slate-500 w-[3rem] h-full rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300" onClick={() => {this.increase_count(); refresh_sum()}}>+</button>
                        <input id={"item_count_".concat(id)} type="text" className="text-center w-[100px] h-full border-slate-300 border-2 outline-none" defaultValue={count}></input>
                        <button className="bg-slate-500 w-[3rem] h-full rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300" onClick={() => {this.decrease_count(); refresh_sum()}}>-</button>
                    </div>
                </div>
                <div className="w-[20%] px-5">
                    <div className="relative top-[50%] translate-y-[-50%]">
                        <span name={"item_price_".concat(id)} className="text-lg  whitespace-nowrap"> {price} </span>
                        <span className="text-lg  whitespace-nowrap"> MC </span>
                    </div>
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
            total: 0
        }
        this.refresh_sum = this.refresh_sum.bind(this)
    }
    componentDidMount(){
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
    refresh_sum(){
        let {item_list} = this.state
        let sum = 0
        for(let i = 0; i < item_list.length; i++){
            count = document.getElementById("item_count_".concat(item_list[i]["id"])).value
            sum += item_list[i]["price"] * count
        }
        this.setState({total: sum})
    }
    render(){
        let {item_list, total} = this.state
        let item_object_list = []
        for(let i = 0; i < item_list.length; i++){
            item_object_list.push(
                <Item
                    id={item_list[i]["id"]}
                    avatar={item_list[i]["avatar"]}
                    count={item_list[i]["count"]}
                    item_name={item_list[i]["name"]}
                    price={item_list[i]["price"]}
                    refresh_sum={this.refresh_sum}>
                </Item>)
        }
        return (
            <div className="w-screen h-fit overflow-y-scroll overflow-x-hidden flex flex-row bg-gray-100">
                <div className="w-[90%] mx-auto h-[80vh] my-[17vh] rounded-md bg-white flex flex-row p-10 gap-5">
                    <div className="w-[80%] h-full">
                        <div className="border-2 h-full p-5 flex flex-col gap-5">
                            {item_object_list}
                        </div>
                    </div>
                    <div className="w-[20%] h-full flex justify-end flex-col gap-5">
                        <div className="h-fit py-5 flex flex-col gap-5 p-5 border-2">
                            <p className="text-2xl font-bold"> 總金額 </p>
                            <p className="md:text-2xl xl:text-4xl font-bold text-blue-500 font-mono"> {total} MC </p>
                        </div>
                        <div className="h-fit">
                            <button className="w-full p-5 bg-blue-400 text-white rounded-md" onClick={() => {window.location.href = "/order_confirmation"}} >確認訂單</button>
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
