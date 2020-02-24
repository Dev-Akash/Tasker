function open_navigation_menu() {
    document.getElementById("navbar").style.display = "block";
}

function close_navigation_menu(params) {
    document.getElementById("navbar").style.display = "none";
}

function checkPass(){
    password = document.getElementById("enter_pass").value
    re_password = document.getElementById("re_enter_pass").value
    if (re_password != password){
        document.getElementById("enter_pass").style.border = "2px solid red"
        document.getElementById("re_enter_pass").style.border = "2px solid red"
    }
    else{
        document.getElementById("enter_pass").style.border = "none"
        document.getElementById("re_enter_pass").style.border = "none"
    }
}

document.getElementById("re_enter_pass").addEventListener('input', checkPass)