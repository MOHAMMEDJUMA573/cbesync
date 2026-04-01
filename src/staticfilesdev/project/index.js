/*~~~~~~~~~~~~~~~ TOGGLE BUTTON ~~~~~~~~~~~~~~~*/
const navMenu = document.getElementById("nav-menu");
const navLinks = document.querySelectorAll(".nav-link");
const hamburger = document.getElementById("hamburger");

hamburger.addEventListener("click", ()=> {
    navMenu.classList.toggle("left-[0]");
    hamburger.classList.toggle("ri-close-large-line");
})

navLinks.forEach((link, index) =>{
    link.addEventListener("click", ()=>{
        navMenu.classList.toggle("left-[0]");
        hamburger.classList.toggle("ri-close-large-line");
    })
})
/*for data urls */
const login = document.getElementById("loginbutton");
login.addEventListener("click", ()=> {
    window.location.href = login.dataset.url;
})
const signin = document.getElementById("signupbutton");
signin.addEventListener("click", ()=> {
    window.location.href = signin.dataset.url
})
/*Scrolls */
const scrollUp = () => {
    const scrollUpButton = document.getElementById("scroll-up")
    if (this.scrollY >= 1000){
        scrollUpButton.classList.remove("-bottom-1/2")
        scrollUpButton.classList.add("bottom-4")
    }else{
        scrollUpButton.classList.add("-bottom-1/2")
        scrollUpButton.classList.remove("bottom-4")
    }
}
window.addEventListener("scroll", scrollUp)
/*Header border*/
const scrollHeader = () => {
    const header = document.getElementById("navbar")
    if (this.scrollY >= 50){
        header.classList.add("border-b", "border-yellow-500")
    }else{
        header.classList.remove("border-b", "border-yellow-500")
    }
}
window.addEventListener("scroll", scrollHeader)
/*Active link show */
const activeLink = () => {
    const sections = document.querySelectorAll("section")
    let current = "home"
    
    sections.forEach((section, index) => {
        const sectionTop = section.offsetTop;
        if (this.scrollY >= sectionTop -60) {
            current = section.getAttribute("id")
        }

    })

    navLinks.forEach((item, index) => {
        item.classList.remove("active")
        if (item.href.includes(current)) {
            item.classList.add("active")
        }
    })
}
window.addEventListener("scroll", activeLink)
