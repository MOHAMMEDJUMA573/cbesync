const teacherRegButton = document.getElementById("teacherReg");
teacherRegButton.addEventListener("click", ()=>{
    window.location.href = teacherRegButton.dataset.url;
})
const studentRegButton = document.getElementById("studentReg");
studentRegButton.addEventListener("click", ()=>{
    window.location.href = studentRegButton.dataset.url;
})
const parentRegButton = document.getElementById("parentReg");
parentRegButton.addEventListener("click", ()=>{
    window.location.href = parentRegButton.dataset.url;
})
const ntstaffRegButton = document.getElementById("ntstaffReg");
ntstaffRegButton.addEventListener("click", ()=>{
    window.location.href = ntstaffRegButton.dataset.url;
})
const teacherEnrollButton = document.getElementById("teacherEnroll");
teacherEnrollButton.addEventListener("click", ()=>{
    window.location.href = teacherEnrollButton.dataset.url;
})
const studentEnroll = document.getElementById("studentEnroll");
studentEnroll.addEventListener("click", ()=>{
    window.location.href = studentEnroll.dataset.url;
})
const parentEnrollButton = document.getElementById("parentEnroll");
parentEnrollButton.addEventListener("click", ()=>{
    window.location.href = parentEnrollButton.dataset.url;
})
const ntstaffEnroll = document.getElementById("ntstaffEnroll");
ntstaffEnroll.addEventListener("click", ()=>{
    window.location.href = ntstaffEnroll.dataset.url;
})
const teacherMngButton = document.getElementById("teacherMng");
teacherMngButton.addEventListener("click", ()=>{
    window.location.href = teacherMngButton.dataset.url;
})
const studentMngButton = document.getElementById("studentMng");
studentMngButton.addEventListener("click", ()=>{
    window.location.href = studentMngButton.dataset.url;
})
const ntstaffMngButton = document.getElementById("ntstaffMng");
ntstaffMngButton.addEventListener("click", ()=>{
    window.location.href = ntstaffMngButton.dataset.url;
})
const parentMngButton = document.getElementById("parentMng");
parentMngButton.addEventListener("click", ()=>{
    window.location.href = parentMngButton.dataset.url;
})
//link active toggle
function T2(){
    /*activate the classlist*/
    document.querySelector(".sidebar a.active")?.classList.remove("active");
    document.querySelectorAll(".sidebar a")[1].classList.add("active");
}
T2();