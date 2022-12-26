class PriceComponent extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            original_price: props.original_price,
            discount_price: props.discount_price
        }
    }
    render(){
        original_price = this.props.original_price
        discount_price = this.props.discount_price
        if(discount_price != original_price){
            return (
                <p className="md:text-base xl:text-2xl font-serif">
                    <span className="pr-5"> NT$ {discount_price} </span>
                    <span className="pr-5 font-bold text-gray-400 line-through"> NT$ {original_price} </span>
                    <span className="pr-5 font-bold"> - {parseFloat((original_price-discount_price)*100/original_price).toFixed(2)} % </span>
                </p>
            )
        }else{
            return (
                <p className="md:text-base xl:text-2xl font-serif">
                    <span className="pr-5"> NT$ {original_price} </span>
                </p>
            )
        }
    }
}

class MainPlatform extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            image_href: undefined,
            name: undefined,
            count: undefined,
            original_price: undefined,
            discount_price: undefined,
            description: ""
        }
        this.increase_count = this.increase_count.bind(this)
    }
    componentDidMount(){
        item_id = window.location.pathname.split("/")[2]
        $.ajax({
            url: "/items/" + item_id,
            method: "GET",
            success: function(data){
                this.setState({
                    image_href: "/static/images/" + data["avatar"],
                    name: data["name"],
                    count: data["count"],
                    original_price: data["price"]["original"],
                    discount_price: data["price"]["discount"],
                    description: data["description"]
                })
            }.bind(this)
        })
    }
    newline_map_description(description){
        if(description == undefined){
            return ""
        }else{
            return description.split("\\n").map((item, idx) => {
                return (
                    <React.Fragment key={idx}>
                        {item}
                        <br />
                    </React.Fragment>
                )
            })
        }
    }
    increase_count(){
        let {count} = this.state
        let value = document.getElementById("order_count_input").value
        let int_value = parseInt(value)
        if(isNaN(int_value)){
            int_value = 0;
        }
        int_value = Math.min(int_value + 1, count)
        document.getElementById("order_count_input").value = int_value
    }
    decrease_count(){
        let value = document.getElementById("order_count_input").value
        let int_value = parseInt(value)
        if(isNaN(int_value)){
            int_value = 0;
        }
        int_value = Math.max(int_value - 1, 0)
        document.getElementById("order_count_input").value = int_value;
    }
    render(){
        let {image_href, name, count, original_price, discount_price, description} = this.state
        return(
            <div className="mt-20 w-full flex flex-col gap-5 top-[8vh] h-fit">
                <div className="flex flex-row justify-even w-[70%] mx-auto p-5">
                    <div className="w-full h-[50vh]">
                        <div className="w-[50vh] h-[50vh] mx-auto p-5 border-2">
                            <img className="w-full h-full object-scale-up" src={image_href}></img>
                        </div>
                    </div>
                    <div className="w-full h-[50vh] flex flex-between flex-col gap-5">
                        <div id="title" className="h-[40%]">
                            <p className="md:text-2xl xl:text-4xl pb-2"> {name} </p>
                            <p className="md:text-sm xl:text-base pb-2 text-gray-500"> 剩餘數量 <span className="underline text-black">{count}</span></p>
                            <PriceComponent original_price={original_price} discount_price={discount_price} />
                        </div>
                        <div id="function" className="h-[40%]">
                            <div>
                                <p className="py-1">數量</p>
                                <div className="flex flex-row h-full">
                                    <button className="bg-slate-500 w-[50px] md:h-[50%] xl:h-[30%] rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300" onClick={() => this.increase_count()}>+</button>
                                    <input type="text" id="order_count_input" className="text-center w-[100px] md:h-[50%] xl:h-[30%] border-slate-300 border-2 outline-none" defaultValue="1"></input>
                                    <button className="bg-slate-500 w-[50px] md:h-[50%] xl:h-[30%] rounded-sm font-mono md:text-base xl:text-2xl text-white hover:bg-slate-400 duration-300" onClick={() => this.decrease_count()}>-</button>
                                </div>
                            </div>
                        </div>
                        <div id="button-set" className="flex flex-row gap-5 h-fit">
                            <button className="py-2 my-auto w-full h-fit bg-amber-500 rounded-md hover:bg-amber-400 duration-300 text-white font-bold shadow-md disabled:bg-slate-400 disabled:text-slate-100" disabled> 直接購買 </button>
                            <button className="py-2 my-auto w-full h-fit bg-orange-500 rounded-md hover:bg-orange-400 duration-300 text-white font-bold shadow-md  disabled:bg-slate-400 disabled:text-slate-100" disabled> 加入購物車 </button>
                        </div>
                    </div>
                </div>
                <hr className="w-[70%] mx-auto" />
                <div className="relative w-[70%] mx-auto text-lg">
                    {this.newline_map_description(description)}
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
