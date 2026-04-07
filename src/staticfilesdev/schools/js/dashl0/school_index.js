//count blobs response
const stdBlob = document.getElementById("studentblob");
stdBlob.addEventListener("click", ()=> {
    window.location.href = stdBlob.dataset.url;
})
const tchBlob = document.getElementById("teacherblob");
tchBlob.addEventListener("click", ()=> {
    window.location.href = tchBlob.dataset.url
})
const ntsBlob = document.getElementById("ntsblob");
ntsBlob.addEventListener("click", ()=> {
    window.location.href = ntsBlob.dataset.url
})
function T2(){
    document.querySelectorAll("#sidebar a")[0].classList.add("active");
}
T2();