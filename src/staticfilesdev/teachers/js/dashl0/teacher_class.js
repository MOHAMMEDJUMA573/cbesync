function CreatePopUp(id){
    const popNode = document.querySelector(id)
    const overlay = popNode.querySelector(".overlay")
    function openPopup(){
        popNode.classList.add("active");
    }
    function closePopup(){
        popNode.classList.remove("active");
    }
    overlay.addEventListener("click", closePopup)
    return openPopup
}

const studentPopup = CreatePopUp("#studentsPopup")
document.querySelector("#studentsView").addEventListener("click", studentPopup)
const teachersPopup = CreatePopUp("#teachersPopup")
document.querySelector("#teachersView").addEventListener("click", teachersPopup)
//link active toggle
function T2(){
    /*activate the classlist*/
    document.querySelector(".sidebar a.active")?.classList.remove("active");
    document.querySelectorAll(".sidebar a")[1].classList.add("active");
}
T2();