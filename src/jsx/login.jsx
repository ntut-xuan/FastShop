function verify_data(email, password){
    let column_set = [email, password]
    let flag = false;
    for(let i = 0; i < 2; i++){
        if(column_set[i].toString().length == 0){
            flag = true;
        }
    }
    return flag;
}

function get_empty_column_message(email, password){
    let column_set = [email, password]
    let column_name = ["信箱", "密碼"]
    let empty_column = []
    for(let i = 0; i < 2; i++){
        if(column_set[i].toString().length == 0){
            empty_column.push(column_name[i])
        }
    }
    return empty_column.join("、") + "未填寫"
}

class LoginPlatform extends React.Component{
    constructor(props){
        super(props)
        this.state = {email: "", password: ""}
        this.handleAccountChange = this.handleAccountChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleAccountChange(event){
        this.setState({email: event.target.value})
    }
    handlePasswordChange(event){
        this.setState({password: event.target.value})
    }
    handleSubmit(event){
        let {email, password} = this.state
        event.preventDefault();
        if(verify_data(email, password)){
            error_swal_with_confirm_button("登入失敗", get_empty_column_message(email, password));
            return;
        }
        $.ajax({
            url: "/login",
            type: "POST",
            data: JSON.stringify({"e-mail": email, "password": password}),
            dataType: "json",
            contentType: "application/json",
            success(data, status, xhr){
                success_swal("登入成功").then(() => {window.location.href = "/"})
            },
            error(xhr, status, error){
                console.log(error)
                if(error == "FORBIDDEN"){
                    error_swal("登入失敗", "帳號或密碼錯誤");
                }else if(error === "UNPROCESSABLE ENTITY"){
                    error_swal("登入失敗", "信箱格式錯誤");
                }else{
                    error_swal("登入失敗", "登入 Payload 格式錯誤，請聯繫管理員");
                }
            }
        })
    }
    render(){
        return (
            <div className="bg-orange-100 w-screen h-screen">
                <form className="w-[600px] max-h-[74vh] bg-white p-10 rounded-lg absolute left-[50%] top-[65%] translate-x-[-50%] translate-y-[-65%] shadow-lg overflow-y-auto" onSubmit={this.handleSubmit}>
                    <div id="title" className="pb-10">
                        <p className="text-center text-2xl"> 登入 </p>
                    </div>
                    <div id="input_group" className="">
                        <input type="text" className="w-full p-3 border-2 border-gray-400 text-xs mb-4 outline-none" placeholder="電子郵件地址" onChange={this.handleAccountChange}></input>
                        <input type="password" className="w-full p-3 border-2 border-gray-400 text-xs mb-4 outline-none" placeholder="密碼" onChange={this.handlePasswordChange}></input>
                    </div>
                    <div id="forgot_password" className="">
                        <p className="text-sm underline underline-offset-2 cursor-pointer"> 忘記密碼？ </p>
                    </div>
                    <div id="button_group" className="pt-10 w-full">
                        <button className="bg-black text-white w-full p-2 my-2"> 登入 </button>
                        <a href="#">
                            <p className="bg-amber-600 text-white w-full p-2 my-2 text-center"> 使用 Google 進行登入 </p>
                        </a>
                    </div>
                    <div id="footer_text" className="text-center pt-10">
                        <p className="my-2"><a href="/register" className="text-sm underline underline-offset-2 my-2 cursor-pointer"> 還沒有帳號嗎？註冊帳號 </a></p>
                        <p className="my-2"><a href="/" className="text-sm underline underline-offset-2 my-2 cursor-pointer"> 返回商店 </a></p>
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
                <LoginPlatform />
            </div>
        )
    }
}

const root = ReactDOM.createRoot(document.getElementById("app"))
root.render(<App />)
