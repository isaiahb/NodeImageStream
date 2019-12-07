// const cv = require("opencv4nodejs");
const path = require("path");
const express = require("express");
const app = express();
const server = require("http").Server(app);
const io = require("socket.io")(server);
const sizeof = require('object-sizeof')

app.use(express.static(__dirname + "/public"));

io.on('connection', function (socket) {
	let id = socket.id;
	console.log("CONNECTED:  " + id)
	socket.on('disconnect', function(){
		console.log("DISCONNECTED:  " + id)
	});

	socket.on("stream", function (data){
		let string = data.toString();
		io.emit('image', string);
	});
});


const port = process.env.PORT || 3000;
server.listen(port);
