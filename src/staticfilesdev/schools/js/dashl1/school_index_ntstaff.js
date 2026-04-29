const ntsSearchTbl = document.getElementById("ntsSearchTbl");
const studentLedger = document.getElementById("nontStaffLedger");
if (ntsSearchTbl != null) {
    studentLedger.classList.add("hidden")
}
function T2(){
    document.querySelectorAll("#sidebar a")[0].classList.add("active");
}
T2();