const sideMenu = document.querySelector("aside");
const menuButton = document.querySelector("#menu-btn");
const closeButton = document.querySelector("#close-btn");
const themeButton = document.querySelector(".theme-toggle-btn");

/*Menu show*/
menuButton.addEventListener('click', ()=> {
    sideMenu.style.display = 'block';
})
/*menu hide*/
closeButton.addEventListener('click', ()=> {
    sideMenu.style.display = 'none';
})
//hide nav bar before proceed
if (window.innerWidth < 768)  {
    const nav_links = document.querySelectorAll(".sidebar a");
    nav_links.forEach((navlink, index) => {
        navlink.addEventListener('click', ()=> {
            sideMenu.style.display = 'none';
        })
    })
}
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
//hide top div
let lastScrollPos = 0;
window.addEventListener('scroll', () => {
    const currentScrollPos = window.pageYOffset || document.documentElement.scrollTop;
    // Only when user has scrolled down at all
    if (window.innerWidth > 768) {
        if (currentScrollPos > 0) {
            document.querySelector(".main-header").style.top = "-3rem";
            document.querySelector(".aside-right .top").style.top = "-3rem";
        }else{
            document.querySelector(".main-header").style.top = "1.5rem";
            document.querySelector(".aside-right .top").style.top = "1.5rem";
        }
    }else{
        if (lastScrollPos > currentScrollPos || lastScrollPos == currentScrollPos) {
            document.querySelector(".main-header").style.top = "0";
            document.querySelector(".aside-right .top").style.top = "0";
        }else{
            document.querySelector(".main-header").style.top = "-5rem";
            document.querySelector(".aside-right .top").style.top = "-5rem";
        }
    }    
    lastScrollPos = currentScrollPos;
});
