function initialize() {
    geocoder = new google.maps.Geocoder();
}

function successFunction(position) {
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;
    codeLatLng(lat, lng)
}

function getCurrentAddress(lat, lng) {

    var latlng = new google.maps.LatLng(lat, lng);

    var location = [];
    location['lat']=lat;
    location['lon']=lng;
    
    geocoder.geocode({'latLng': latlng}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        console.log(results)
        if (results[1]) {
         //formatted address
         alert(results[0].formatted_address)
         location['formatted_address'] = results[0].formatted_address;
         
         //find country name
         for (var i=0; i<results[0].address_components.length; i++) {
           for (var b=0; b<results[0].address_components[i].types.length;b++) {
            //there are different types that might hold a city admin_area_lvl_1
            // usually does in come cases looking for sublocality type will be
            // more appropriate
                if (results[0].address_components[i].types[b] 
                              == "administrative_area_level_1") {
                    //this is the object you are looking for
                    state= results[0].address_components[i];
                    
                }

                if (results[0].address_components[i].types[b] 
                              == "administrative_area_level_2") {
                    //this is the object you are looking for
                    city= results[0].address_components[i];
                    
                }
            }
        }
        //city data
        location['state'] = state.long_name;
        location['city'] = city.long_name;


        document.getElementById('id_location_formatted_address').value = "LOCATION: "+location['city'] + ", "+location['state']; 
        document.getElementById('id_location_lat').value = location['lat'];
        document.getElementById('id_location_lon').value = location['lon'];
              
        return location;

        } else {
          alert("No results found");
        }
      } else {
        alert("Geocoder failed due to: " + status);
      }
    });
    
  }

function foundLocation(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    var userLocation = lat + ', ' + lon;
    alert(userLocation);
    var currentLocation = getCurrentAddress(lat,lon);

    document.getElementById('id_location_formatted_address').value = currentLocation['formatted_address'];
        
}

  
  
function noLocation(error) {
  if (err.code == 1) {
    alert("User said no!");
  }
}

function getLocation() {
  if (Modernizr.geolocation) {
    initialize();
    navigator.geolocation.getCurrentPosition(foundLocation, noLocation);
  } else {
    // no native support; maybe try Gears?
  }
}


// Popup menu with sub menus
var menu = new goog.ui.PopupMenu();

menu.attach(document.getElementById('menu1'),
    goog.positioning.Corner.BOTTOM_START);
menu.addItem(new goog.ui.MenuItem('Current Location'));
menu.addItem(new goog.ui.MenuItem('Anywhere'));
menu.render();

goog.events.listen(menu, 'action', function(e) {
  var action = e.target.getValue();
  
  if (action == 'Current Location'){
    getLocation();
  }  
});  

// Filters in adventure index and search pages
goog.events.listen(categoryMenu, goog.ui.Component.EventType.ACTION,
  function(e) {
    var select = e.target;
    var value = select.getValue();
    var tag = document.getElementById("tag");
    alert(value);
    tag.value = value;
    alert(tag.value);
    document.forms['adventures-search-form'].submit();
    //goog.dom.setTextContent(goog.dom.getElement('category-menu'), value);
    
});

goog.events.listen(priceMenu, goog.ui.Component.EventType.ACTION,
  function(e) {
    var select = e.target;
    var value = select.getValue();
    alert(value);
    //goog.dom.setTextContent(goog.dom.getElement('price-menu'), value);
    
});





