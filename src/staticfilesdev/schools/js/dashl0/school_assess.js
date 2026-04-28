const stdTbl = document.getElementById("stdtblbody");
const mainBody = document.querySelector("body");
const toggleButtons = document.querySelectorAll(".toggles");
//link active toggle
function T2(){
    /*activate the classlist*/
    document.querySelectorAll("#sidebar a")[3].classList.add("active");
}
T2();
//
if (stdTbl != null) {
    stdTbl.addEventListener("scroll", ()=> {
        window.location.href = "#stdtblbody"
    })
}
mainBody.addEventListener("scroll", ()=> {
    window.location.href = "#"
})
// configure select from buttons 
toggleButtons.forEach((toggleb, index) => {
    //set the value
    const original_state = toggleb.querySelector("p").innerText
    if (original_state == '1'){
        toggleb.classList.toggle("bg-background");
        toggleb.classList.toggle("bg-activeb");
        toggleb.classList.toggle("justify-end");
        if (index == 0 || index == 2) {
            toggleb.querySelector("select").value = 1;
        }
    }else{
        if (index == 0 || index == 2) {
            toggleb.querySelector("select").value = 0
        }
    }
    toggleb.addEventListener("click", ()=> {
        let boolValue = toggleb.classList.toggle("justify-end");
        toggleb.classList.toggle("bg-activeb");
        toggleb.classList.toggle("bg-background");
        if (index == 0 || index == 2) {
            if (boolValue){
                toggleb.querySelector("select").value = 1
            }else{
                toggleb.querySelector("select").value = 0
            }
        }
    })
})
//hide management on results view
const rViewDiv = document.getElementById("rclassinfo");
if (rViewDiv != null) {
    const rConfigForm = document.getElementById("rconfigForm");
    rConfigForm.classList.add("hidden")
}