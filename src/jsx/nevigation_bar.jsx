let clickable_text = "h-full transition-all duration-200 hover:bg-gray-400 hover:text-white px-5 cursor-pointer"

class AuthenticationComponent extends React.Component {
    constructor(props){
        super(props)
    }
    render(){
        let block_style = "relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"
        let block_text = ""
        let block_url = ""
        if(this.props.login == false){
            block_text = "登入"
            block_url = "/login"
        }else{
            block_text = this.props.username
            block_url = "/profile"
        }
        return (
            <a href={block_url}>
                <div className={clickable_text}>
                    <p className={block_style}>{block_text}</p>
                </div>
            </a>
        )
    }
}

class NevigationBar extends React.Component {
    constructor(props){
        super(props);
        this.state = {login: false, username: null}
        this.nav_extend_on = this.nav_extend_on.bind(this);
        this.nav_extend_off = this.nav_extend_off.bind(this);
        this.check_jwt_verify = this.check_jwt_verify.bind(this)
    }
    nav_extend_on(){
        document.getElementById("nav_extend_main").classList.remove("h-0")
        document.getElementById("nav_extend_main").classList.add("h-80")
    }
    nav_extend_off(){
        document.getElementById("nav_extend_main").classList.remove("h-80")
        document.getElementById("nav_extend_main").classList.add("h-0")
    }
    check_jwt_verify(){
        $.ajax({
            url: "/verify_jwt",
            type: "POST",
            success: function(data, status, xhr){
                this.setState({login: true, username: data["data"]["firstname"] + " " + data["data"]["lastname"]})
            }.bind(this)
        })
    }
    componentDidMount(){
        this.check_jwt_verify()
    }
    render(){
        let {username, login} = this.state
        return [
            <div className="w-full fixed top-0 left-0 z-20 bg-white">
                <div className="w-[90%] mx-auto h-20 flex flex-row relative left-0 top-0">
                    <div className="w-full h-full gap-5 flex-row flex justify-start text-sm text-center">
                        <img className="h-full w-auto py-5" src="/static/image/fastshop.svg"></img>
                        <a href="/">
                            <div className={clickable_text}>
                                <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]">首頁</p>
                            </div>
                        </a>
                        <a href="/items_list">
                            <div className={clickable_text} onMouseOver={this.nav_extend_on} onMouseOut={this.nav_extend_off}>
                                <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]">所有商品</p>
                            </div>
                        </a>
                        <div className={clickable_text}>
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]">最新消息</p>
                        </div>
                        <div className={clickable_text}>
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]">聯繫我們</p>
                        </div>
                    </div>
                    <div className="w-[50%] h-full mx-auto gap-5 flex-row flex justify-end text-sm text-center">
                        <div className={clickable_text}>
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]">搜尋</p>
                        </div>
                        <AuthenticationComponent username={username} login={login} />
                        <div className={clickable_text}>
                            <p className="relative top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]">購物車</p>
                        </div>
                    </div>
                </div>
            </div>
        ]
    }
}
