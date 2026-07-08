// ======================================================
// AI Portrait Editor
// script.js (Part 1)
// ======================================================

// -----------------------------
// Fabric Canvas
// -----------------------------

const canvas = new fabric.Canvas("editorCanvas", {
    preserveObjectStacking: true,
    selection: false
});

canvas.setWidth(400);
canvas.setHeight(400);

// -----------------------------
// Elements
// -----------------------------

const imageInput = document.getElementById("imageInput");
const loadingBox = document.getElementById("loadingBox");
const backgroundPreview = document.getElementById("backgroundPreview");
const zoomSlider = document.getElementById("zoomSlider");

const bgThumbs = document.querySelectorAll(".bg-thumb");

let portrait = null;

let originalScale = 1;

let originalLeft = 200;

let originalTop = 200;

// -----------------------------
// Upload Image
// -----------------------------

imageInput.addEventListener("change", uploadImage);

async function uploadImage() {

    const file = imageInput.files[0];

    if (!file) return;

    loadingBox.style.display = "block";

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch("/process-image", {

            method: "POST",

            body: formData

        });

        if (!response.ok) {

            throw new Error("Processing failed.");

        }

        const blob = await response.blob();

        const imageURL = URL.createObjectURL(blob);

        loadPortrait(imageURL);

    }

    catch (err) {

        alert(err.message);

        console.log(err);

    }

    finally {

        loadingBox.style.display = "none";

    }

}

// -----------------------------
// Load Processed Portrait
// -----------------------------

function loadPortrait(imageURL) {

    if (portrait) {

        canvas.remove(portrait);

    }

    fabric.Image.fromURL(imageURL, function(img) {

        portrait = img;

        portrait.set({

            originX: "center",

            originY: "center",

            left: 200,

            top: 200,

            selectable: true,

            hasBorders: false,

            hasControls: false,

            lockRotation: true

        });

        const maxSize = 280;

        const scale = Math.min(

            maxSize / img.width,

            maxSize / img.height

        );

        portrait.scale(scale);

        originalScale = scale;

        originalLeft = 200;

        originalTop = 200;

        canvas.add(portrait);

        canvas.setActiveObject(portrait);

        canvas.renderAll();

        zoomSlider.value = 100;

    });

}

// -----------------------------
// Background Selection
// -----------------------------

bgThumbs.forEach(function(thumb){

    thumb.addEventListener("click", function(){

        bgThumbs.forEach(function(img){

            img.classList.remove("active");

        });

        this.classList.add("active");

        backgroundPreview.src = this.src;

    });

});

// -----------------------------
// Zoom
// -----------------------------

zoomSlider.addEventListener("input", function(){

    if(!portrait) return;

    const scale = originalScale * (this.value / 100);

    portrait.scale(scale);

    canvas.renderAll();

});

// ======================================================
// PART 2
// Controls + Download
// ======================================================

// -----------------------------
// Move Buttons
// -----------------------------

const moveUp = document.getElementById("moveUp");
const moveDown = document.getElementById("moveDown");
const moveLeft = document.getElementById("moveLeft");
const moveRight = document.getElementById("moveRight");

const centerBtn = document.getElementById("centerBtn");
const resetBtn = document.getElementById("resetBtn");
const downloadBtn = document.getElementById("downloadBtn");

// Move Distance

const STEP = 5;

// -----------------------------
// Move Up
// -----------------------------

moveUp.addEventListener("click", function(){

    if(!portrait) return;

    portrait.top -= STEP;

    canvas.renderAll();

});

// -----------------------------
// Move Down
// -----------------------------

moveDown.addEventListener("click", function(){

    if(!portrait) return;

    portrait.top += STEP;

    canvas.renderAll();

});

// -----------------------------
// Move Left
// -----------------------------

moveLeft.addEventListener("click", function(){

    if(!portrait) return;

    portrait.left -= STEP;

    canvas.renderAll();

});

// -----------------------------
// Move Right
// -----------------------------

moveRight.addEventListener("click", function(){

    if(!portrait) return;

    portrait.left += STEP;

    canvas.renderAll();

});

// -----------------------------
// Center Image
// -----------------------------

centerBtn.addEventListener("click", function(){

    if(!portrait) return;

    portrait.left = 200;
    portrait.top = 200;

    canvas.renderAll();

});

// -----------------------------
// Reset
// -----------------------------

resetBtn.addEventListener("click", function(){

    if(!portrait) return;

    portrait.left = originalLeft;

    portrait.top = originalTop;

    portrait.scale(originalScale);

    zoomSlider.value = 100;

    canvas.renderAll();

});

// -----------------------------
// Keyboard Arrows
// -----------------------------

document.addEventListener("keydown", function(e){

    if(!portrait) return;

    switch(e.key){

        case "ArrowUp":
            portrait.top -= STEP;
            break;

        case "ArrowDown":
            portrait.top += STEP;
            break;

        case "ArrowLeft":
            portrait.left -= STEP;
            break;

        case "ArrowRight":
            portrait.left += STEP;
            break;

        default:
            return;

    }

    canvas.renderAll();

});

// -----------------------------
// Double Click = Center
// -----------------------------

canvas.on("mouse:dblclick", function(){

    if(!portrait) return;

    portrait.left = 200;
    portrait.top = 200;

    canvas.renderAll();

});

// -----------------------------
// Download JPG
// -----------------------------

downloadBtn.addEventListener("click", function(){

    // Create temporary canvas

    const exportCanvas = document.createElement("canvas");

    exportCanvas.width = 400;
    exportCanvas.height = 400;

    const ctx = exportCanvas.getContext("2d");

    // Draw Background

    const bg = new Image();

    bg.crossOrigin = "anonymous";

    bg.onload = function(){

        ctx.drawImage(bg,0,0,400,400);

        // Draw Fabric Canvas

        const fg = new Image();

        fg.onload = function(){

            ctx.drawImage(fg,0,0);

            const link = document.createElement("a");

            link.download = "portrait.jpg";

            link.href = exportCanvas.toDataURL(
                "image/jpeg",
                0.95
            );

            link.click();

        };

        fg.src = canvas.toDataURL({

            format:"png",

            multiplier:1

        });

    };

    bg.src = backgroundPreview.src;

});

// ======================================================
// Keep Image Inside Canvas
// ======================================================

canvas.on("object:moving", function(e){

    const obj = e.target;

    if(!obj) return;

    obj.setCoords();

    if(obj.left < 0)
        obj.left = 0;

    if(obj.top < 0)
        obj.top = 0;

    if(obj.left > 400)
        obj.left = 400;

    if(obj.top > 400)
        obj.top = 400;

});

// ======================================================
// Better Cursor
// ======================================================

canvas.on("mouse:down", function(){

    canvas.defaultCursor = "grabbing";

});

canvas.on("mouse:up", function(){

    canvas.defaultCursor = "grab";

});