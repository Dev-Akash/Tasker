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

document.getElementById("re_enter_pass").addEventListener('input', checkPass)

document.getElementById("useremail").addEventListener('blur', checkEmail)

function fetchProjects(){
    var all_projects = new Array();
    //An abstract class for Projects.
    class Project{
        constructor(id, name, des, dead, owner, team){
            this.id = id;
            this.name = name;
            this.des = des;
            this.dead = dead;
            this.owner = owner;
            this.team = team;
        }
        getID(){return this.id;}
        getName(){return this.name;}
        getDescription(){return this.des;}
        getDeadline(){return this.dead;}
        getOwner(){return this.owner;}
        getTeamMembers(){return this.team;}
        setID(id){this.id = id;}
        setName(name){this.name = name;}
        setDescription(des){this.des = des;}
        setDeadline(deadline){this.dead = deadline}
        setOwner(owner){this.owner = owner}
        setTeamMembers(member){this.team = member;}
    }
    //Requesting the server for return JSON of all projects.
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.status == 200 & this.readyState == 4){
            var json_output = JSON.parse(this.responseText);
            var owned_arr = json_output.owned;
            var associated_arr = json_output.associated;
            //Adding owned projects in array
            for (i in owned_arr){
                var arr = owned_arr[i];
                temp = new Project(arr.project_id,arr.project_name, arr.project_des, arr.project_dead, arr.project_owner, arr.project_team);
                all_projects.push(temp);
            }
            //Adding associated projects in array
            for (i in associated_arr){
                var arr = associated_arr[i];
                temp = new Project(arr.project_id,arr.project_name, arr.project_des, arr.project_dead, arr.project_owner, arr.project_team);
                all_projects.push(temp);
            }
            //Creating and adding Cards to index Page
            addCards(all_projects, owned_arr.length, associated_arr.length);
        } 
    }
    xhttp.open("POST", '/fetchProjects')
    xhttp.send()  
}

function addCards(projects, olen, alen){
    var count = 1;
    for (i in projects){
        //Creating inner content card of Project such as "Name"
        var divv = document.createElement("div");
        divv.className = "project_card_content";
        divv.innerHTML = projects[i].getName();
        //Creating the clickable element to wrap the above div
        var elem = document.createElement("a");
        elem.className = "project_card";
        elem.href = "/project_dash?id="+projects[i].getID();
        if (i < olen){
            elem.style.background = "purple";
        }
        else{
            elem.style.background = "orange";
        }
        elem.appendChild(divv);
        //Adding the whole element to body now.
        document.body.appendChild(elem);
        count++;
    }
}

var hide_n_seek_tap = 0;
function hide_n_seek_menu(){
    if (hide_n_seek_tap == 0){
        document.getElementById("new_task_button").style.display = "none";
        document.getElementById("new_stage_button").style.display = "none";
        hide_n_seek_tap = 1;   
    }
    else{
        document.getElementById("new_task_button").style.display = "block";
        document.getElementById("new_stage_button").style.display = "block";
        hide_n_seek_tap = 0;
    }
}
var prompt_task = 0;
function prompt_task_dialogue(){
    if (prompt_task == 0){
        document.getElementById("new_task_dialogue").style.display = "block";
    }
    else{
        document.getElementById("new_task_dialogue").style.display = "none";
    }
}
