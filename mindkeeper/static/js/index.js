username = document.querySelector(".profile")
profileMenu = document.querySelector(".profile_menu")

username.addEventListener('onmouseover', function (){
    profileMenu.classList.add('.active')
    console.log('enter')

})
username.addEventListener('onmouseout', function (){
    profileMenu.classList.remove('.active')
    console.log('leave')
})