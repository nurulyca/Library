document.addEventListener('DOMContentLoaded', function() {
    console.log('load');
    console.log(window.location.search.split("?"))
    let params = window.location.search.split("?")[1]
    params = params.split("=")
    let id = params[1]
    getUserById(id)
    .then(res => {
        let name = document.querySelector(".detail-name")
        name.innerHTML = res.name
        let email = document.querySelector(".detail-email")
        email.innerHTML = res.email
        let password = document.querySelector(".detail-password")
        password.innerHTML = res.password
        let username = document.querySelector(".detail-username")
        username.innerHTML = res.username
    })
  });


function getUserById(id) {
    return fetch("http://127.0.0.1:5000/users/" + id + "/")
    .then(res => res.json())
    .then(jsonRes => jsonRes)
}