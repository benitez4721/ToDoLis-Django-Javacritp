

document.addEventListener('DOMContentLoaded', () => {
    load_login()
})

function load_login() {
    document.querySelector('#login-link').classList.add('active')
    document.querySelector('#register-link').classList.remove('active')
    document.querySelector('#register-form').style.display = 'none'
    document.querySelector('#login-form').style.display = 'flex'
}

function load_register(){
    document.querySelector('#register-link').classList.add('active')
    document.querySelector('#login-link').classList.remove('active')
    document.querySelector('#register-form').style.display = 'flex'
    document.querySelector('#login-form').style.display = 'none'
}

function register(){
    const username = document.querySelector('#username1').value
    const email = document.querySelector('#email1').value
    const password = document.querySelector('#password1').value
    const confirmation = document.querySelector('#confirmation').value

    fetch("/register",{
        method : 'POST',
        body: JSON.stringify({
            username,
            email,
            password,
            confirmation
        })
    })
    .then( resp => resp.json())
    .then( resp => console.log(resp))
}

function login(){
    const username = document.querySelector("#username").value
    const password = document.querySelector("#password").value

    fetch("/login",{
        method: "POST",
        body : JSON.stringify({
            username,
            password
        })
    })
    .then( resp => resp.json())
    .then( resp => {
        console.log("login")
        let url = window.location.href
        window.location.href = `${url}main`
        // document.querySelector('#auth').style.display = 'none'
        // document.querySelector('#main').style.display = 'block'

    })
}