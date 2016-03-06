function initMap() {
	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 4,
	});

	for school in schools:
		var lat_long = get_lat_long(school["address"])
		var marker = new google.maps.Marker({
			position: lat_long
			map: map
			title: school["name"]
		})

	



}