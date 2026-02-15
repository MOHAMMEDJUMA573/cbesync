//custom auto pop 15/02/2025
const classdivs = document.querySelectorAll(".main-c-part");
classdivs.forEach((div, index) => {
    const divPopups = div.querySelectorAll(".popup");
    const divButtons = div.querySelectorAll(".class-opts")
    divPopups.forEach((pop, index) => {
        const popoverlay = pop.querySelector(".overlay")
        function openPopup(){
            pop.classList.add("active");
        }
        function closePopup(){
            pop.classList.remove("active");
        }
        popoverlay.addEventListener("click", closePopup)
        divButtons.forEach((but, index2) => {
            if (index2 == index) {
                but.addEventListener("click", openPopup)
            }
        });
    });
});

function T2(){
    /*activate the classlist*/
    document.querySelector(".sidebar a.active")?.classList.remove("active");
    document.querySelectorAll(".sidebar a")[1].classList.add("active");
}
T2();