const sideMenu = document.querySelector("aside");
const menuButton = document.querySelector("#menu-btn");
const closeButton = document.querySelector("#close-btn");
const themeButton = document.getElementById("#theme-toggle-btn");
const topBar = document.getElementById("topbar")

/*Menu show*/
menuButton.addEventListener('click', ()=> {
    sideMenu.classList.toggle("-left-full");
})
/*menu hide*/
closeButton.addEventListener('click', ()=> {
    sideMenu.classList.toggle("-left-full");
})
//hide nav bar before proceed
if (window.innerWidth < 768)  {
    const nav_links = document.querySelectorAll("#sidebar a");
    nav_links.forEach((navlink, index) => {
        navlink.addEventListener('click', ()=> {
            sideMenu.classList.add("-left-full");
        })
    })
}
// //hide top div
let lastScrollPos = 0;
window.addEventListener('scroll', () => {
    const currentScrollPos = window.pageYOffset || document.documentElement.scrollTop;
    // Only when user has scrolled down at all
    if (window.innerWidth > 1024) {
        if (currentScrollPos > 50) {
            topBar.classList.add("hidden");
        }else{
            topBar.classList.remove("hidden");
        }
    }else{
        if (lastScrollPos > currentScrollPos || lastScrollPos == currentScrollPos) {
            topBar.classList.remove("hidden");
        }else if(currentScrollPos > 100){
            topBar.classList.add("hidden");
        }
    }    
    lastScrollPos = currentScrollPos;
});
//
function T1(){
    document.body.classList.toggle('dark-theme-variables');
    /*change the button style after toggle*/
    themeButton.querySelector('span:nth-child(1)').classList.toggle('active');
    themeButton.querySelector('span:nth-child(2)').classList.toggle('active');
}
/*theme changer*/
themeButton.addEventListener('click', ()=> {
    const currentTheme = document.documentElement.getAttribute('data-theme')
    if (currentTheme == 'dark') {
        document.documentElement.setAttribute('data-theme', 'light');
    }else if(currentTheme == 'light'){
        // document.documentElement.setAttribute('data-theme', 'volcano');
    // }else if(currentTheme == 'volcano'){
        // document.documentElement.setAttribute('data-theme', 'forest');
    
    // }else{
        document.documentElement.setAttribute('data-theme', 'dark');
    }
})
// window.onpopstate = function() {
//    console.log("poped")
// }