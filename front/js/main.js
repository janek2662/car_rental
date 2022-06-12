
function login(){
    var url = "http://localhost:5000/login";
    var login = document.getElementById("usr").value;
    var pwd = document.getElementById("pwd").value;
    // var base64 = btoa(login+":"+pwd)

    http_request = new XMLHttpRequest();
    http_request.withCredentials = true;

    http_request.open('POST', url, true);
    
    var params = new FormData();
    params.append('login', login);
    params.append('password', pwd);

    http_request.send(params);

    http_request.onload = function(xhr) {
        if (xhr.target.status == 200) {
            // console.log(http_request.getResponseHeader("Set-Cookie"));
            // document.cookie = http_request.getResponseHeader("Set-Cookie");
            
            // if(login == "admin") {
            //     sessionStorage.setItem("is_admin", "true");
            // }
            // sessionStorage.setItem("is_logged", "true");
            // sessionStorage.setItem("pass", base64);
            // window.location.href = "http://localhost:3000/dashboard.html";
        } else {
            document.getElementById("error").innerHTML = "Niepoprawna nazwa użytkownika lub hasło";
        }
    }

}

function register(){
    var url = "http://localhost:5000/register";
    var login = document.getElementById("usr").value;
    var pwd = document.getElementById("pwd").value;
    var pwdRepeat = document.getElementById("pwdRepeat").value;

    if((login !="") && (pwd != "") && (pwdRepeat != "")) {
        if (pwd == pwdRepeat) {
            http_request = new XMLHttpRequest();
            http_request.open('POST', url, true)

            var params = new FormData();
            params.append('login', login);
            params.append('password', pwd);

            http_request.send(params);
            http_request.onload=function(xhr) {
                if (xhr.target.status == 201) {
                    window.location.href = "http://localhost:3000";
                } else {
                    document.getElementById("error").innerHTML = "Niepoprawna nazwa użytkownika lub hasło";
                }
            }
        } else {
            document.getElementById("error").innerHTML = "Podane hasła różnią się"
        }
    } else {
        document.getElementById("error").innerHTML = "Brakujące dane"
    }


}


// function logout(){
//     sessionStorage.setItem("isLogged", "false");
//     sessionStorage.setItem("isAdmin", "false");
//     sessionStorage.setItem("pass", "");
// }

// function showBooks() {
//     var url = "http://localhost:8080/SimpleLibrarySpring/dashboard/";
//     var base64 = sessionStorage.getItem("pass");
//     var userLogged = sessionStorage.getItem("isLogged");
//     var isAdmin = sessionStorage.getItem("isAdmin");
//
//     http_request = new XMLHttpRequest();
//     http_request.onload = function(xhr) {
//         if (xhr.target.status == 200 && userLogged == "true") {
//             var data = JSON.parse(xhr.target.response);
//             if(isAdmin == "true") {
//                 document.getElementById("data").innerHTML =
//                     data.map(function(val) { return "<tr><th id ="+val.id+" scope='row'>"
//                         +val.id+"</th><td>"+val.title+"</td><td>"+val.author+"</td><td>"+val.year
//                         +"</td><td><button type='button' class='btn btn-primary' onclick={deleteBook("+val.id+")};window.location.reload();>Usuń książkę</button></td></tr>" ; }).join('');
//             } else {
//                 document.getElementById("data").innerHTML =
//                     data.map(function(val) { return "<tr><th id ="+val.id+" scope='row'>"
//                         +val.id+"</th><td>"+val.title+"</td><td>"+val.author+"</td><td>"+val.year
//                         +"</td><td></td></tr>" ; }).join('');
//             }
//         } else {
//             window.location.href = "http://localhost:3000/index.html";
//         }
//     }
//
//     http_request.open('GET', url, true);
//     http_request.setRequestHeader("Authorization", "Basic "+ base64);
//     http_request.send(null);
// }
//
// function addBook() {
//     var url = "http://localhost:8080/SimpleLibrarySpring/dashboard/";
//     var base64 = sessionStorage.getItem("pass");
//     var userLogged = sessionStorage.getItem("isLogged");
//     var isAdmin = sessionStorage.getItem("isAdmin");
//
//     const dataToSend = {
//         author:document.getElementById("author").value,
//         title:document.getElementById("title").value,
//         year:document.getElementById("year").value
//     }
//
//     http_request = new XMLHttpRequest();
//     if(isAdmin == "true") {
//         var jsonString = JSON.stringify(dataToSend);
//         http_request.open('POST', url);
//         http_request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
//         http_request.setRequestHeader("Authorization", "Basic "+ base64);
//         http_request.send(jsonString);
//         document.getElementById("meassage").innerHTML = "Książka dodana";
//     }
// }
//
// function showAddForm(){
//     var isAdmin = sessionStorage.getItem("isAdmin");
//
//     if(isAdmin == "true"){
//         document.getElementById("bookadd").innerHTML =   "<div class='col-lg-6 text-center'>"
//             +"   <h1 class='mt-5'>Dodaj książkę</h1>"
//             +"   <form>"
//             +"   <div class='form-group'>"
//             +"     <input type='text' class='form-control' id='author' placeholder='Autor' required>"
//             +"     <input type='text' class='form-control' id='title' placeholder='Tytuł' required'>"
//             +"      <input type='text' class='form-control' id='year' placeholder='Rok wydania' required>"
//             +"     </div>"
//             +"   </form>"
//             +"   <button type='button' class='btn btn-primary' onclick={addBook()};window.location.reload();>Dodaj książkę</button>"
//             +" </div>"
//             +" <p class='text-danger' style='margin-left: 45%; margin-top: 10%' id='meassage'></p>"
//             +"</div>";
//     }else{
//         document.getElementById("bookadd").innerHTML = "Nieautoryzowany dostęp (tylko dla ADMINA)";
//     }
// }
//
// function deleteBook(id) {
//     var url = "http://localhost:8080/SimpleLibrarySpring/dashboard/"+id;
//     var base64 = sessionStorage.getItem("pass");
//     var userLogged = sessionStorage.getItem("isLogged");
//
//     http_request = new XMLHttpRequest();
//     http_request.open('DELETE', url, true);
//     http_request.setRequestHeader("Authorization", "Basic "+ base64);
//     http_request.send(null);
// }
