console.log('hello')
const home = document.getElementById('home')
const login = document.getElementById('login')
const table = document.getElementById('table')
const register = document.getElementById('register')

if(window.location.pathname === '/index'){
    home.classList.add('active')

} else if(window.location.pathname === '/login'){
    login.classList.add('active')

}else if(window.location.pathname === '/table'){
    table.classList.add('active')

}else if(window.location.pathname === '/register'){
    register.classList.add('active')

}
