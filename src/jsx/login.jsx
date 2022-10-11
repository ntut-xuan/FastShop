
class LoginPlatform extends React.Component{
    render(){
        return (
            <div className="bg-orange-100 w-screen h-screen">
                <div className="w-[600px] h-fit bg-white p-10 rounded-lg absolute left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] shadow-lg">
                    <div id="title" className="pb-10">
                        <img className="w-24 h-auto mx-auto my-2 rounded-full" src="https://ntut-xuan.github.io/src/image/fastshop.png"></img>
                        <p className="text-center text-2xl"> 登入 </p> 
                    </div>
                    <div id="input_group" className="">
                        <input type="text" className="w-full p-3 border-2 border-gray-400 text-xs mb-4 outline-none" placeholder="電子郵件地址"></input>
                        <input type="password" className="w-full p-3 border-2 border-gray-400 text-xs mb-4 outline-none" placeholder="密碼"></input>
                    </div>
                    <div id="forgot_password" className="">
                        <p className="text-sm underline underline-offset-2 cursor-pointer"> 忘記密碼？ </p> 
                    </div>
                    <div id="button_group" className="pt-10">
                        <button className="bg-black text-white w-full p-2 my-2"> 登入 </button>
                        <button className="bg-amber-600 text-white w-full p-2 my-2"> 使用 Google 進行登入 </button>
                    </div>
                    <div id="footer_text" className="text-center pt-10">
                        <p className="my-2"><a href="/register" className="text-sm underline underline-offset-2 my-2 cursor-pointer"> 還沒有帳號嗎？註冊帳號 </a></p>
                        <p className="my-2"><a href="/" className="text-sm underline underline-offset-2 my-2 cursor-pointer"> 返回商店 </a></p>
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
                <LoginPlatform />
            </div>
        )
    }
}

const root = ReactDOM.createRoot(document.getElementById("app"))
root.render(<App />)
