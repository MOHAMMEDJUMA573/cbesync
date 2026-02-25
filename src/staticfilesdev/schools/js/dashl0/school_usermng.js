//selected grids
grid_partitions = document.querySelectorAll(".grid-partitions")
grid_partitions.forEach( (partition, index) => {
    partition.addEventListener("click", ()=> {
        window.location.href = partition.dataset.url
    })
});
//link active toggle
function T2(){
    /*activate the classlist*/
    document.querySelectorAll(".sidebar a")[1].classList.add("active");
}
T2();