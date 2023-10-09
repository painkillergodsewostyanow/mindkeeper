const singInBtn = document.querySelector('.sing_in-btn')
const singUnBtn = document.querySelector('.sing_up-btn')
const formBox = document.querySelector('.form-box')
const body = document.body

singUnBtn.addEventListener('click', function (){
    formBox.classList.add('active')
    body.classList.add('active')
})

singInBtn.addEventListener('click', function (){
    formBox.classList.remove('active')
    body.classList.remove('active')
})