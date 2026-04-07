//count blobs response
ledgerdivs = document.querySelectorAll(".school-l-div")
ledgerdivs.forEach( (ldiv,index) => {
    ldiv.addEventListener("click", ()=> {
        window.location.href = ldiv.dataset.url
    })
})
function T2(){
    document.querySelectorAll("#sidebar a")[0].classList.add("active");
}
T2();