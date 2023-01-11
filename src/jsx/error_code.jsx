function success_swal(title){
    return Swal.fire({
        icon: "success",
        title: title,
        timer: 1500,
        showConfirmButton: false
    })
}

function error_swal(title, text){
    return Swal.fire({
        icon: "error",
        title: title,
        text: text,
        timer: 1500,
        showConfirmButton: false
    })
}

function error_swal_with_confirm_button(title, text){
    return Swal.fire({
        icon: "error",
        title: title,
        text: text,
        showConfirmButton: true
    })
}
