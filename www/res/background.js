var background_turtles = [
    ["#e4883f", 1],
    ["#f7e73a", 3],
    ["#7f7f7f", 8],
    ["#584944", 0],
    ["#13a5de", 2],
    ["#e91c21", 7],
    ["#7f7f7f", 6]
];

function background_render() {
    var canvas = document.getElementById("background");
    var turtles = [];

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    var offset = -50;
    for (var info of background_turtles) {
	var t = canvas.getContext("2d");
	turtles.push(t);

	t._totalLength = info[1];
	t.strokeStyle = info[0];
	t.lineCap = "round";
	t.lineWidth = 10;
	t.moveTo(canvas.width, canvas.height + offset);

	offset += 20;
    }

    var len = 0;
    function step() {
	for (var t of turtles) {
	    
	    len += 1;
	}
    }
}

window.addEventListener("load", background_render);
window.addEventListener("resize", background_render);
