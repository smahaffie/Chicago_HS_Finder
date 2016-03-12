'''Javascript version of create_map.py; contains code
for generating map from Google Maps API'''


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