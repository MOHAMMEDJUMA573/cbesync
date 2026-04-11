//link active toggle
function T2(){
    /*activate the classlist*/
    document.querySelectorAll("#sidebar a")[3].classList.add("active");
}
T2();
//
const stdTbl = document.getElementById("stdtblbody")
const mainBody = document.querySelector("body")
stdTbl.addEventListener("scroll", ()=> {
    window.location.href = "#stdtblbody"
})
mainBody.addEventListener("scroll", ()=> {
    window.location.href = "#"
})