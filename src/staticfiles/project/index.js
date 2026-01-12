const themeButton = document.querySelector(".theme-toggle-btn");
//
function T1(){
    document.body.classList.toggle('dark-theme-variables');
    /*change the button style after toggle*/
    themeButton.querySelector('span:nth-child(1)').classList.toggle('active');
    themeButton.querySelector('span:nth-child(2)').classList.toggle('active');
}
/*theme changer*/
themeButton.addEventListener('click', ()=> {
    T1();
})