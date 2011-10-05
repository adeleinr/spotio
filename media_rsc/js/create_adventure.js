  var defaultBounds = new google.maps.LatLngBounds(
  new google.maps.LatLng(-33.8902, 151.1759),
  new google.maps.LatLng(-33.8474, 151.2631));

  var input = document.getElementById('id_location_formatted_address');
  var options = {
    bounds: defaultBounds,
    types: ['geocode']
  };

  autocomplete = new google.maps.places.Autocomplete(input, options);

  google.maps.event.addListener(autocomplete, 'place_changed', function() {
    var place = autocomplete.getPlace();
    alert(place.formatted_address);
    alert(place.geometry.location.lat());
    alert(place.geometry.location.lng());
 
    var id_location_formatted_address = document.getElementById('id_location_formatted_address');
    id_location_formatted_address.value = place.formatted_address;
    
    var id_location_lat = document.getElementById('id_location_lat');
    id_location_lat.value = place.geometry.location.lat();
    
    var id_location_lon = document.getElementById('id_location_lon');
    id_location_lon.value = place.geometry.location.lng();
    
  });
