
class RegisterPlatform extends React.Component{
    render(){
        return (
            <div className="bg-blue-100 w-screen h-screen">
                <div className="w-[600px] h-fit bg-white p-10 rounded-lg absolute left-[50%] top-[55%] translate-x-[-50%] translate-y-[-50%] shadow-lg">
                    <div id="title" className="pb-10">
                        <p className="text-center text-2xl"> 註冊 </p> 
                    </div>
                    <div id="input_group" className="flex flex-col gap-3">
                        <div className="flex flex-row gap-3">
                            <input type="text" className="w-full p-3 border-2 border-gray-400 text-xs outline-none" placeholder="姓氏"></input>
                            <input type="text" className="w-full p-3 border-2 border-gray-400 text-xs outline-none" placeholder="名稱"></input>
                        </div>
                        <div className="flex flex-row gap-3">
                            <select className="w-full p-3 border-2 border-gray-400 text-xs outline-none" defaultValue="性別">
                                <option className="w-full text-xs" disabled="disabled">性別</option>
                                <option className="w-full text-xs">男性</option>
                                <option className="w-full text-xs">女性</option>
                            </select>
                            <input type="text" className="w-full p-3 border-2 border-gray-400 text-xs outline-none" placeholder="出生日期" data-toggle="datepicker"></input>
                        </div>
                        <input type="text" className="w-full p-3 border-2 border-gray-400 text-xs outline-none" placeholder="電子郵件地址"></input>
                        <input type="password" className="w-full p-3 border-2 border-gray-400 text-xs outline-none" placeholder="密碼"></input>
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
                        <button className="bg-blue-600 text-white w-full p-2 my-2"> 使用 Google 進行註冊 </button>
                    </div>
                    <div id="footer_text" className="text-center pt-10">
                        <p className="my-2"><a href="/login" className="text-sm underline underline-offset-2 cursor-pointer"> 已經有帳號了？登入帳號 </a></p>
                        <p className="my-2"><a href="/" className="text-sm underline underline-offset-2 cursor-pointer"> 返回商店 </a></p>
                    </div>
                </div>
            </div>
        )
    }
}

class App extends React.Component {
    componentDidMount(){
        $('[data-toggle="datepicker"]').datepicker({
            format: 'yyyy-mm-dd'
        });
    }
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
