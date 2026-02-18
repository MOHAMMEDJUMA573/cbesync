function T2(){
    /*activate the classlist*/
    document.querySelector(".sidebar a.active")?.classList.remove("active");
    document.querySelectorAll(".sidebar a")[2].classList.add("active");
}
T2();