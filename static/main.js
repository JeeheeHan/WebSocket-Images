$(document).ready( ()=>{

	const socket = io.connect();

	socket.on('connect', () => {
		console.log("hello");
	});

	$('#addedImage').on('change', function(e) {
		let file = e.originalEvent.target.files[0],
			reader = new FileReader();
 
		reader.onload = function(evt) {
			const jsonObject = {
					'imageData': evt.target.result
				}
 
			// send a custom socket message to server
			socket.emit('new image', jsonObject);
		};
 
		reader.readAsDataURL(file);
	});


	socket.on('add image',(res)=>{
		$('#chatbox').append('<img src="'+res.imageData+'"/>')
	});

});
