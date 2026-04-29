const stdSearchTbl = document.getElementById("stdSearchTbl");
const studentLedger = document.getElementById("studentLedger");
if (stdSearchTbl != null) {
    studentLedger.classList.add("hidden")
}
function T2(){
    document.querySelectorAll("#sidebar a")[0].classList.add("active");
}
T2();