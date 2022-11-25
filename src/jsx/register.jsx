
class RegisterPlatform extends React.Component{
    constructor(props){
        super(props)
        this.state = {firstname: "", lastname: "", gender: -1, birthday: "", email: "", password: ""}
        this.handleFirstnameChange = this.handleFirstnameChange.bind(this);
        this.handleLastnameChange = this.handleLastnameChange.bind(this);
        this.handleGenderChange = this.handleGenderChange.bind(this);
        this.handleEmailChange = this.handleEmailChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleFirstnameChange(event){
        this.setState({firstname: event.target.value})
    }
    handleLastnameChange(event){
        this.setState({lastname: event.target.value})
    }
    handleGenderChange(event){
        this.setState({gender: event.target.value})
    }
    handleEmailChange(event){
        this.setState({email: event.target.value})
    }
    handlePasswordChange(event){
        this.setState({password: event.target.value})
    }
    handleSubmit(event){
        let {firstname, lastname, gender, birthday, email, password} = this.state
        let payload = JSON.stringify({
            "e-mail": email,
            "password": password,
            "firstname": firstname,
            "lastname": lastname,
            "gender": gender,
            "birthday": birthday
        })
        console.log(payload)
        event.preventDefault();
        $.ajax({
            url: "/register",
            type: "POST",
            data: payload,
            dataType: "json",
            contentType: "application/json",
            success(data, status, xhr){
                success_swal("註冊成功").then(() => {window.location.href = "/"})
            },
            error(xhr, status, error){
                console.log(error)
                if(error == "FORBIDDEN"){
                    error_swal("註冊失敗", "帳號已存在");
                }else if(error === "UNPROCESSABLE ENTITY"){
                    error_swal("註冊失敗", "註冊資料格式錯誤");
                }else{
                    error_swal("註冊失敗", "註冊 Payload 格式錯誤，請聯繫管理員");
                }
            }
        })
    }
    componentDidMount(){
        $('[data-toggle="datepicker"]').datepicker({
            onSelect: function(date) {
                this.setState({birthday: date})
            }.bind(this),
            dateFormat: 'yy-mm-dd',
            yearRange: "1900:2022",
            changeYear: true,
            changeMonth: true,
            minDate: null,
            maxDate: 0,
        })
    }
    render(){
        return (
            <div className="bg-blue-100 w-screen h-screen">
                <form className="w-[600px] h-fit bg-white p-10 rounded-lg absolute left-[50%] top-[55%] translate-x-[-50%] translate-y-[-50%] shadow-lg" onSubmit={this.handleSubmit}>
                    <div id="title" className="pb-10">
                        <p className="text-center text-2xl"> 註冊 </p>
                    </div>
                    <div id="input_group" className="flex flex-col gap-3">
                        <div className="flex flex-row gap-3">
                            <input type="text" className="w-full p-3 border-2 border-gray-400 text-xs outline-none" placeholder="姓氏" onChange={this.handleFirstnameChange}></input>
                            <input type="text" className="w-full p-3 border-2 border-gray-400 text-xs outline-none" placeholder="名稱" onChange={this.handleLastnameChange}></input>
                        </div>
                        <div className="flex flex-row gap-3">
                            <select className="w-full p-3 border-2 border-gray-400 text-xs outline-none" defaultValue="性別" onChange={this.handleGenderChange}>
                                <option className="w-full text-xs" disabled="disabled">性別</option>
                                <option className="w-full text-xs" value="0">男性</option>
                                <option className="w-full text-xs" value="1">女性</option>
                            </select>
                            <input type="text" className="w-full p-3 border-2 border-gray-400 text-xs outline-none" placeholder="出生日期" data-toggle="datepicker"></input>
                        </div>
                        <input type="text" className="w-full p-3 border-2 border-gray-400 text-xs outline-none" placeholder="電子郵件地址" onChange={this.handleEmailChange}></input>
                        <input type="password" className="w-full p-3 border-2 border-gray-400 text-xs outline-none" placeholder="密碼" onChange={this.handlePasswordChange}></input>
                    </div>
                    <div id="declare" className="py-5">
                        <p className="text-sm">
                            一旦點擊註冊，即表示你同意 FastShop 的
                            <a className="text-sm decoration-black underline underline-offset-2 cursor-pointer">服務條款</a>，
                            <a className="text-sm underline underline-offset-2 cursor-pointer">隱私政策</a>和
                            <a className="text-sm underline underline-offset-2 cursor-pointer">退款政策</a>。
                        </p>
                    </div>
                    <div id="button_group" className="">
                        <button className="bg-black text-white w-full p-2 my-2"> 註冊 </button>
                        <a href="#">
                            <p className="bg-blue-600 text-white w-full p-2 my-2 text-center"> 使用 Google 進行註冊 </p>
                        </a>
                    </div>
                    <div id="footer_text" className="text-center pt-10">
                        <p className="my-2"><a href="/login" className="text-sm underline underline-offset-2 cursor-pointer"> 已經有帳號了？登入帳號 </a></p>
                        <p className="my-2"><a href="/" className="text-sm underline underline-offset-2 cursor-pointer"> 返回商店 </a></p>
                    </div>
                </form>
            </div>
        )
    }
}

class App extends React.Component {
    render(){
        return (
            <div className="">
                <NevigationBar />
                <RegisterPlatform />
            </div>
        )
    }
}

const root = ReactDOM.createRoot(document.getElementById("app"))
root.render(<App />)
