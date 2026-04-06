const sideMenu = document.querySelector("aside");
const menuButton = document.querySelector("#menu-btn");
const closeButton = document.querySelector("#close-btn");
const themeButton = document.querySelector(".theme-toggle-btn");

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