//selected options
sections_options = document.querySelectorAll(".tmngopt")
sections_options.forEach( (section, index) => {
    if (index == 0 || index == 1) {
        section.addEventListener("click", ()=> {
            window.location.href = section.dataset.url
        })
    }
});
//link active toggle
function T2(){
    /*activate the classlist*/
    document.querySelectorAll("#sidebar a")[1].classList.add("active");
}
T2();