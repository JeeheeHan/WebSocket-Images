$(document).ready( ()=>{

	const socket = io.connect();
	//initiate socket.io library

	socket.on('connect', () => {
	});

	$('#addedImage').on('change', function(e) {
		//wait for file to be added then send to server as base64 string in a dictionary form
		let file = e.originalEvent.target.files[0];
		reader = new FileReader();
 
		reader.onload = function(evt) {
			let jsonObject = {
					'imageData': evt.target.result
				};
 
			// send a custom socket message to server
			socket.emit('new image', jsonObject);
		};
 
		reader.readAsDataURL(file);
	});


	socket.on('add image',(res)=>{
		//From server get image path to add into DOM and focus view to the added image
		$('.imagechatbox').append('<img src='+res.imagePath+' class="imagesize"/>')
		$('.imagechatbox').scrollTop($('.imagechatbox')[0].scrollHeight);
	});

});
