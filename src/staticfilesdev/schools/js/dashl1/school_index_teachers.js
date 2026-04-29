const tchSearchTbl = document.getElementById("tchSearchTbl");
const teacherLedger = document.getElementById("teacherLedger");
if (tchSearchTbl != null) {
    teacherLedger.classList.add("hidden")
}
function T2(){
    document.querySelectorAll("#sidebar a")[0].classList.add("active");
}
T2();