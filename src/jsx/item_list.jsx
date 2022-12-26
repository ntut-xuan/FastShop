class TagSection extends React.Component {
    constructor(props){
        super(props)
        this.state = {tags: [], handler: props.handler}
        this.click = this.click.bind(this)
    }
    componentDidMount(){
        $.ajax({
            url: "/tags",
            method: "GET",
            success: function(data){
                this.setState({tags: data["tags"]})
            }.bind(this)
        })
    }
    click(name){
        let {handler} = this.state
        handler(name)
    }
    render(){
        let {tags} = this.state
        array = []
        for(let i = 0; i < tags.length; i++){
            let name = tags[i]["name"];
            array.push(
                <button className="p-2 w-full text-center" onClick={() => this.click(name)}>{name}</button>
            )
        }
        return(
            <div className="overflow-y-auto h-[75vh] pt-5">
                <div className="py-5">
                    {array}
                </div>
                <button className="p-2 w-full text-center border-2" onClick={() => this.click(undefined)}>清除篩選</button>
            </div>
        )
    }
}

class PriceSection extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            original_price: props.original_price,
            discount_price: props.discount_price,
        }
    }
    render(){
        let {original_price, discount_price} = this.state
        let price = [<p className="text-center"> {discount_price} MC </p>]
        let discount_percentage = "-" + parseFloat(original_price/discount_price).toFixed(2) + "%"
        if(original_price != discount_price){
            price.push(
                <p className="text-center text-sm">
                    <span className="line-through"> {original_price} MC </span>
                    <span>&nbsp;</span>
                    <span className="font-bold"> {discount_percentage} </span>
                </p>
            )
        }
        return price
    }
}

class ItemObject extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            id: props.id,
            detail_href: props.detail_href,
            image_href: props.image_href,
            name: props.name,
            original_price: props.original_price,
            discount_price: props.discount_price
        }
    }
    render(){
        let {id, detail_href, image_href, name, original_price, discount_price} = this.state
        return (
            <a className="h-fit w-fit" href={detail_href}>
                <div className="p-5 w-fit h-fit">
                    <div id={"items_image_" + {id}} className="w-[30vh] h-[30vh] border-2 mx-auto p-5">
                        <img className="w-full h-full object-scale-up" src={image_href}></img>
                    </div>
                    <p className="text-center p-2"> {name} </p>
                    <PriceSection original_price={original_price} discount_price={discount_price} />
                </div>
            </a>
        )
    }
}

class ItemSection extends React.Component {
    constructor(props){
        super(props)
        this.state = {item: []}
    }
    componentDidMount(){
        $.ajax({
            url: "/items",
            method: "GET",
            success: function(data){
                if(data){
                    this.setState({item: data})
                }
            }.bind(this)
        })
    }
    should_filter(item_data, filter_tags){
        if(filter_tags != undefined){
            tags = item_data["tags"]
            for(let i = 0; i < tags.length; i++){
                if(tags[i]["name"] == filter_tags){
                    return true;
                }
            }
            return false;
        }
        return true;
    }
    render(){
        let {item} = this.state
        let filter_tags = this.props.filter_tags
        array = []
        for(let i = 0; i < item.length; i++){
            item_data = item[i]
            if(!this.should_filter(item_data, filter_tags)){
                continue;
            }
            array.push(
                <ItemObject
                    id={item_data["id"]}
                    detail_href={"/items_list/" + item_data["id"]}
                    image_href={"/static/images/" + item_data["avatar"]}
                    name={item_data["name"]}
                    original_price={item_data["price"]["original"]}
                    discount_price={item_data["price"]["discount"]}
                />
            )
        }
        return (
            <div className="w-full overflow-y-auto h-[75vh] grid grid-cols-3">
                {array}
            </div>
        )
    }
}

class MainPlatform extends React.Component {
    constructor(props){
        super(props)
        this.state = {filter_tags: undefined}
        this.tags_filter_handler = this.tags_filter_handler.bind(this)
    }
    tags_filter_handler(value){
        this.setState({
            filter_tags: value
        })
    }
    render(){
        let {filter_tags} = this.state
        return (
            <div className="mt-20 fixed w-full">
                <div className="w-[80%] h-screen mx-auto flex flex-row gap-5 my-10">
                    <div className="w-[30%]">
                        <p className="w-full text-center p-5 text-2xl"> 類別 </p>
                        <hr />
                        <TagSection handler={this.tags_filter_handler}/>
                    </div>
                    <div className="w-[70%]">
                        <p className="w-full text-center p-5 text-2xl"> 所有商品 </p>
                        <hr />
                        <ItemSection filter_tags={filter_tags}/>
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
