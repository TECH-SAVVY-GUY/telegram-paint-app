const canvas = document.querySelector("#canvas");
const toolbar = document.getElementById("tool-bar");
const ctx = canvas.getContext('2d');

window.addEventListener("load", () => {
    const stroke = document.querySelector("#slider");
    const color = document.querySelector("#color");
    const canvasOffsetY = canvas.offsetTop;

    canvas.height = 0.9 * (window.innerHeight - toolbar.clientHeight);
    canvas.width = toolbar.clientWidth;

    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    let painting = false;

    function startPosition(e) {
        painting = true;
        draw(e);
    }

    function finishedPosition() {
        painting = false;
        ctx.beginPath();
    }

    function draw(e) {
        e.preventDefault(); // Prevent scrolling on mobile devices

        let clientX, clientY;

        if (e.type === "mousemove") {
            clientX = e.clientX;
            clientY = e.clientY;
        } else if (e.type === "touchmove") {
            clientX = e.touches[0].clientX;
            clientY = e.touches[0].clientY;
        }

        if (!painting) return;

        ctx.lineWidth = stroke.value;
        ctx.lineCap = "round";
        ctx.strokeStyle = color.value;
        ctx.lineTo(clientX - 20, clientY - canvasOffsetY);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(clientX - 20, clientY - canvasOffsetY);
    }

    canvas.addEventListener("mousedown", startPosition);
    canvas.addEventListener("mouseup", finishedPosition);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("touchstart", startPosition);
    canvas.addEventListener("touchend", finishedPosition);
    canvas.addEventListener("touchmove", draw);
    canvas.addEventListener("touchcancel", finishedPosition);

});

const eraseBtn = document.querySelector(".erase-button");
eraseBtn.addEventListener("click", clear);

function clear() {
    var canvas = document.querySelector("#canvas");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

const saveBtn = document.querySelector(".save-button");
saveBtn.addEventListener("click", save);

function save() {
    var canvas = document.querySelector("#canvas");

    fetch('/paintResponse', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            imageData: canvas.toDataURL(),
            initData: window.Telegram.WebApp.initData
        })
    });
}

Telegram.WebApp.ready();
Telegram.WebApp.expand();
