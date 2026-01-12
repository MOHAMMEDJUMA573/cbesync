//count blobs response
const stdBlob = document.getElementById("studentblob");
stdBlob.addEventListener("click", ()=> {
    window.location.href = "dashl1/school_index_students.html"
})
const tchBlob = document.getElementById("teacherblob");
tchBlob.addEventListener("click", ()=> {
    window.location.href = "dashl1/school_index_teachers.html"
})
const ntsBlob = document.getElementById("ntsblob");
ntsBlob.addEventListener("click", ()=> {
    window.location.href = "dashl1/school_index_ntstaff.html"
})


//drawing canvas
const percento = document.querySelector(".percentNo").innerText;
const size = 100;
//function to draw the circle
for (let i = 0; i <= 2; i++) {
    const circleS = "canvas" + i;
    const canvas = document.querySelector(`.${circleS}`);
    canvas.width = size;
    canvas.height = size;
    //styling
    canvas.style.border = "3px solid"
    canvas.style.margin = "5px";
    //
    const ctx = canvas.getContext("2d");
    drawCircle(ctx, i+1);
}

function drawCircle(ctx, method) {
    ctx.translate(size/2, size/2);
    ctx.beginPath();
    ctx.lineWidth = 3;
    const rad = size * 0.4;
    //
    switch (method) {
        case 1: {
            ctx.strokeStyle = 'green';
            ctx.lineWidth = 8;
            ctx.arc(0, 0, rad, 0, Math.PI * ((1/3)*2));
            break;
        }
        case 2: {
            ctx.strokeStyle = 'green';
            ctx.lineWidth = 8;
            ctx.arc(0, 0, rad, 0, Math.PI * ((1/3)*2));
            break;
        }
        case 3: {
            ctx.strokeStyle = 'green';
            ctx.lineWidth = 8;
            ctx.arc(0, 0, rad, 0, Math.PI * ((1/3)*2));
            break;
        }
    }
    
    ctx.stroke();
}