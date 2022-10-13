class HeaderImage extends React.Component {
    render(){
        return (
            <div className="relative w-full h-full bg-[url('/static/image/advertisement.jpg')]">
                <div className="w-full h-full bg-black bg-opacity-50 absolute">
                    <div className="absolute left-[10%] bottom-[30%] border-l-2 border-white p-5">
                        <p className="text-6xl text-white py-3"> FastShop </p>
                        <p className="text-3xl text-white py-3"> Fast, simple, convenient. </p>
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
                <HeaderImage />
            </div>
        )
    }
}

const root = ReactDOM.createRoot(document.getElementById("app"))
root.render(<App />)
