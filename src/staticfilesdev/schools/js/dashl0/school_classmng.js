const clsTbl = document.getElementById("clstblbody")
const mainBody = document.querySelector("body")
classOpts = document.querySelectorAll(".classes_opts")

//help  in table scroll
clsTbl.addEventListener("scroll", ()=> {
    window.location.href = "#clstblbody"
})
mainBody.addEventListener("scroll", ()=> {
    window.location.href = "#"
})
//select options urls
classOpts.forEach( (partition, index) => {
    if (index > -1 && index < 2) {
        partition.addEventListener("click", ()=> {
            window.location.href = partition.dataset.url
        })
    }
});
//link active toggle
function T2(){
    /*activate the classlist*/
    document.querySelectorAll("#sidebar a")[2].classList.add("active");
}
T2();