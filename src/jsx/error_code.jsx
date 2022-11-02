const ERROR_CODE = Object.freeze({
    "INVALID_DATA": {"code": 301, "message": "未知的資料"},
    "INVALID_EMAIL": {"code": 302, "message": "信箱格式錯誤"},
    "INCORRECT_LOGIN": {"code": 401, "message": "登入失敗，帳號或密碼錯誤"}
})

function getMessageFromCode(code){
    let keys = Object.keys(ERROR_CODE)
    for(let i = 0; i < keys.length; i++){
        let key = keys[i];
        if(parseInt(ERROR_CODE[key]["code"]) === code){
            console.log(code)
            return ERROR_CODE[key]["message"]
        }
    }
}

function success_swal(title){
    return Swal.fire({
        icon: "success",
        title: title,
        timer: 1500,
        showConfirmButton: false
    })
}

function error_swal(title, code){
    Swal.fire({
        icon: "error",
        title: title,
        text: getMessageFromCode(code),
        timer: 1500,
        showConfirmButton: false
    })
}
