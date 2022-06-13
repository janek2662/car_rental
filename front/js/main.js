
function start(){
    showCars();
    showReservations();
    showAddReservationForm();
    showPatchForm();
    showAddCarForm();
    showDeleteCarForm();
}

function login(){
    var url = "http://localhost:5000/login";
    var login = document.getElementById("usr").value;
    var pwd = document.getElementById("pwd").value;

    http_request = new XMLHttpRequest();
    http_request.withCredentials = true;

    http_request.open('POST', url, true);
    
    var params = new FormData();
    params.append('login', login);
    params.append('password', pwd);

    http_request.send(params);

    http_request.onload = function(xhr) {
        if (xhr.target.status == 200) {
            window.location.href = "http://localhost:3000/dashboard.html";
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

function showCars() {
    var url = "http://localhost:5000/car";
    var base64 = sessionStorage.getItem("pass");
    // var userLogged = sessionStorage.getItem("isLogged");
    var userLogged = "true";
    var isAdmin = sessionStorage.getItem("is_admin");
    
    http_request = new XMLHttpRequest();
    http_request.withCredentials = true;
    http_request.open('GET', url, true);
    http_request.onload = function(xhr) {
        var data = JSON.parse(xhr.target.response);
        document.getElementById("data").innerHTML =
            data.map(function(val) { return "<tr><th id ="+val.id+" scope='row'>"
                +val.id+"</th><td>"+val.brand+"</td><td>"+val.version+"</td><td>"+val.year
                +"</td><td></td></tr>" ; }).join('');
    }

    http_request.send(null);
}

function showReservations() {
    var url = "http://localhost:5000/reservation";
    var base64 = sessionStorage.getItem("pass");
    // var userLogged = sessionStorage.getItem("isLogged");
    var userLogged = "true";
    var isAdmin = sessionStorage.getItem("is_admin");
    
    http_request = new XMLHttpRequest();
    http_request.open('GET', url, true);
    http_request.withCredentials = true;
    http_request.onload = function(xhr) {
        var data = JSON.parse(xhr.target.response);
        document.getElementById("reservations").innerHTML =
            data.map(function(val) { return "<tr><th id ="+val.id+" scope='row'>"
                +val.id+"</th><td>"+val.car_id+"</td><td>"+val.date_from+"</td><td>"+val.date_to
                +"</td><td><button type='button' class='btn btn-primary' onclick={deleteReservation("+val.id+")};>Usuń Rezerwacje</button></td></tr>" ; }).join('');
    }

    http_request.send(null);
}

// function showCars() {
//     var url = "http://localhost:5000/dashboard";
//     var base64 = sessionStorage.getItem("pass");
//     var userLogged = sessionStorage.getItem("isLogged");
//     var isAdmin = sessionStorage.getItem("isAdmin");

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

//     http_request.open('GET', url, true);
//     http_request.setRequestHeader("Authorization", "Basic "+ base64);
//     http_request.send(null);
// }
//
// function addCar() {
//     var url = "http://localhost:8080/SimpleLibrarySpring/dashboard/";
//     var base64 = sessionStorage.getItem("pass");
//     var userLogged = sessionStorage.getItem("isLogged");
//     var isAdmin = sessionStorage.getItem("isAdmin");

//     const dataToSend = {
//         author:document.getElementById("author").value,
//         title:document.getElementById("title").value,
//         year:document.getElementById("year").value
//     }

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
// function showAddReservationForm(){
//     var isAdmin = sessionStorage.getItem("isAdmin");

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
function deleteReservation(id) {
    var url = "http://localhost:5000/reservation/"+id;
    var base64 = sessionStorage.getItem("pass");
    var userLogged = sessionStorage.getItem("isLogged");

    http_request = new XMLHttpRequest();
    http_request.withCredentials = true;
    http_request.open('DELETE', url, true);
    // http_request.setRequestHeader("Authorization", "Basic "+ base64);
    http_request.send(null);
}

function deleteCar() {
    var url = "http://localhost:5000/car/"+document.getElementById("car_id").value;
    var base64 = sessionStorage.getItem("pass");
    var userLogged = sessionStorage.getItem("isLogged");

    http_request = new XMLHttpRequest();
    http_request.withCredentials = true;
    http_request.open('DELETE', url, true);
    // http_request.setRequestHeader("Authorization", "Basic "+ base64);
    http_request.send(null);
}

function showAddReservationForm(){
    var isAdmin = sessionStorage.getItem("isAdmin");
    var isAdmin = "true"
    if(isAdmin == "true"){
        document.getElementById("reservationadd").innerHTML =   "<div class='col-lg-6 text-center'>"
            +"   <h1 class='mt-5'>Dodaj rezerwacje</h1>"
            +"   <form>"
            +"   <div class='form-group'>"
            +"     <input type='text' class='form-control' id='car_id' placeholder='Identyfikator samochodu' required>"
            +"     <input type='text' class='form-control' id='date_from' placeholder='Od YYYY-MM-DD' required'>"
            +"      <input type='text' class='form-control' id='date_to' placeholder='Do YYYY-MM-DD' required>"
            +"     </div>"
            +"   </form>"
            +"   <button type='button' class='btn btn-primary' onclick={addReservation()};>Dodaj rezerwacje</button>"
            +" </div>"
            +" <p class='text-danger' style='margin-left: 45%; margin-top: 10%' id='meassage'></p>"
            +"</div>";
    }else{
        document.getElementById("reservationadd").innerHTML = "Nieautoryzowany dostęp (tylko dla ADMINA)";
    }
}

function showPatchForm(){
    var isAdmin = sessionStorage.getItem("isAdmin");
    var isAdmin = "true"
    if(isAdmin == "true"){
        document.getElementById("reservationpatch").innerHTML =   "<div class='col-lg-6 text-center'>"
            +"   <h1 class='mt-5'>Zmodyfikuj rezerwacje</h1>"
            +"   <form>"
            +"   <div class='form-group'>"
            +"     <input type='text' class='form-control' id='reservation_id' placeholder='Identyfikator rezerwacji' required>"
            +"     <input type='text' class='form-control' id='date_from' placeholder='Od YYYY-MM-DD' required'>"
            +"      <input type='text' class='form-control' id='date_to' placeholder='Do YYYY-MM-DD' required>"
            +"     </div>"
            +"   </form>"
            +"   <button type='button' class='btn btn-primary' onclick={patchReservation()};>Zmodyfikuj rezerwacje</button>"
            +" </div>"
            +" <p class='text-danger' style='margin-left: 45%; margin-top: 10%' id='meassage'></p>"
            +"</div>";
    }else{
        document.getElementById("reservationpatch").innerHTML = "Nieautoryzowany dostęp (tylko dla ADMINA)";
    }
}

function showAddCarForm(){
    var isAdmin = sessionStorage.getItem("isAdmin");
    var isAdmin = "true"
    if(isAdmin == "true"){
        document.getElementById("caradd").innerHTML =   "<div class='col-lg-6 text-center'>"
            +"   <h1 class='mt-5'>Dodaj samochod</h1>"
            +"   <form>"
            +"   <div class='form-group'>"
            +"     <input type='text' class='form-control' id='car_id' placeholder='Identyfikator samochodu' required>"
            +"     <input type='text' class='form-control' id='brand' placeholder='Marka auta' required'>"
            +"      <input type='number' class='form-control' id='version' placeholder='Wersja auta' required>"
            +"      <input type='number' class='form-control' id='year' placeholder='Rok produkcji' required>"
            +"     </div>"
            +"   </form>"
            +"   <button type='button' class='btn btn-primary' onclick={addCar()};>Dodaj samochod</button>"
            +" </div>"
            +" <p class='text-danger' style='margin-left: 45%; margin-top: 10%' id='meassage'></p>"
            +"</div>";
    }else{
        document.getElementById("caradd").innerHTML = "Nieautoryzowany dostęp (tylko dla ADMINA)";
    }
}

function showDeleteCarForm(){
    var isAdmin = sessionStorage.getItem("isAdmin");
    var isAdmin = "true"
    if(isAdmin == "true"){
        document.getElementById("cardelete").innerHTML =   "<div class='col-lg-6 text-center'>"
            +"   <h1 class='mt-5'>Usun samochod</h1>"
            +"   <form>"
            +"   <div class='form-group'>"
            +"     <input type='number' class='form-control' id='car_id' placeholder='Identyfikator samochodu' required>"
            +"     </div>"
            +"   </form>"
            +"   <button type='button' class='btn btn-primary' onclick={deleteCar()};>Usun samochod</button>"
            +" </div>"
            +" <p class='text-danger' style='margin-left: 45%; margin-top: 10%' id='meassage'></p>"
            +"</div>";
    }else{
        document.getElementById("cardelete").innerHTML = "Nieautoryzowany dostęp (tylko dla ADMINA)";
    }
}

function addReservation() {
    var url = "http://localhost:5000/reservation";
    // var base64 = sessionStorage.getItem("pass");
    // var userLogged = sessionStorage.getItem("isLogged");
    // var isAdmin = sessionStorage.getItem("isAdmin");
    var isAdmin = "true";

    const dataToSend = {
        car_id:document.getElementById("car_id").value,
        date_from:document.getElementById("date_from").value,
        date_to:document.getElementById("date_to").value
    }

    http_request = new XMLHttpRequest();
    http_request.withCredentials = true;
    if(isAdmin == "true") {
        var jsonString = JSON.stringify(dataToSend);
        http_request.open('POST', url);
        http_request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        // http_request.setRequestHeader("Authorization", "Basic "+ base64);
        http_request.send(jsonString);
        document.getElementById("meassage").innerHTML = "Rezerwacja dodana";
    }
}

function patchReservation() {
    var url = "http://localhost:5000/reservation";
    // var base64 = sessionStorage.getItem("pass");
    // var userLogged = sessionStorage.getItem("isLogged");
    // var isAdmin = sessionStorage.getItem("isAdmin");
    var isAdmin = "true";

    const dataToSend = {
        reservation_id:document.getElementById("reservation_id").value,
        date_from:document.getElementById("date_from").value,
        date_to:document.getElementById("date_to").value
    }

    http_request = new XMLHttpRequest();
    http_request.withCredentials = true;
    if(isAdmin == "true") {
        var jsonString = JSON.stringify(dataToSend);
        http_request.open('PATCH', url);
        http_request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        // http_request.setRequestHeader("Authorization", "Basic "+ base64);
        http_request.send(jsonString);
        document.getElementById("meassage").innerHTML = "Rezerwacja dodana";
    }
}


function addCar() {
    // var url = "http://localhost:5000/car";
    // var base64 = sessionStorage.getItem("pass");
    // var userLogged = sessionStorage.getItem("isLogged");
    // var isAdmin = sessionStorage.getItem("isAdmin");
    var isAdmin = "true";

    const dataToSend = {
        brand:document.getElementById("brand").value,
        version:document.getElementById("version").value,
        year:document.getElementById("year").value
    }

    var url = "http://localhost:5000/car/" + document.getElementById("car_id").value;
    http_request = new XMLHttpRequest();
    http_request.withCredentials = true;
    if(isAdmin == "true") {
        var jsonString = JSON.stringify(dataToSend);
        http_request.open('PUT', url);
        http_request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        // http_request.setRequestHeader("Authorization", "Basic "+ base64);
        http_request.send(jsonString);
        document.getElementById("meassage").innerHTML = "Samochód dodany";
    }
}