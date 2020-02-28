function open_navigation_menu() {
    document.getElementById("navbar").style.display = "block";
}

function close_navigation_menu(params) {
    document.getElementById("navbar").style.display = "none";
}

function checkPass(){
    password = document.getElementById("enter_pass").value;
    re_password = document.getElementById("re_enter_pass").value;
    if (re_password != password){
        document.getElementById("enter_pass").style.border = "2px solid red";
        document.getElementById("re_enter_pass").style.border = "2px solid red";
        document.getElementById("sign_up_button").disabled = true;
        document.getElementById("sign_up_button").style.opacity = 0.5;
    }
    else{
        document.getElementById("enter_pass").style.border = "none";
        document.getElementById("re_enter_pass").style.border = "none";
        document.getElementById("sign_up_button").disabled = false;
        document.getElementById("sign_up_button").style.opacity = 1;
    }
}

function checkEmail(){
    var email = document.getElementById("useremail").value
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.status == 200 & this.readyState ==4){
            var res = this.responseText;
            if (res == "True"){
                document.getElementById("useremail").style.border = "2px solid red";
            }
            else{
                document.getElementById("useremail").style.border = "none";
            }
        }
    }
    xhttp.open("POST", "checkEmail?email="+email)
    xhttp.send()
}

function fetchProjects(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.status == 200 & this.readyState == 4){
            var res = this.responseText;
        } 
    }
    xhttp.open("POST", '/fetchProjects')
    xhttp.send()
}

document.getElementById("re_enter_pass").addEventListener('input', checkPass)

document.getElementById("useremail").addEventListener('blur', checkEmail)