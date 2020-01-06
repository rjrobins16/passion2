function PrimpMap(locations = stylists) {
    var bounds = new google.maps.LatLngBounds();
    var mapType = {mapTypeId: 'roadmap'};
    var markers = [];
    var infoWindowContent = [];
    var map = new google.maps.Map(document.getElementById('stylist-near-you-map'),mapType);

    map.setTilt(45);

    locations.forEach(function (location) {
        markers.push([location.fields.BusinessName, location.fields.lat,location.fields.lng]);
        infoWindowContent.push([location.fields.businessname +
        + location.fields.address + location.fields.city +
        location.fields.state + location.fields.zip ]);

    });

    var infoWindow = new google.maps.InfoWindow(),marker, i;

    for(i=0; i<markers.length; i++){
        var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
        bounds.extend(position);
        marker = new google.maps.Marker({
            position:position,
            map:map,
            title:markers[i][0]
        });

        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infoWindow.setContent(infoWindowContent[i][0]);
                infoWindow.open(map, marker);
            }
        })(marker, i));

        if (locations.length > 1) {
            map.fitBounds(bounds);
        } else {
            var center = new google.maps.LatLng(locations[0].fields.lat, locations[0].fields.lng);
            map.setCenter(center);
            map.setZoom(15);
        }

    }
}
function filterLocations() {
    var userLatLng;
    var geocoder = new google.maps.Geocoder();
    var userAddress = document.getElementById('userAddress').value.replace(/[^a-z0-9\s]/gi, '');
    var maxRadius = parseInt(document.getElementById('maxRadius').value, 10);

    if (userAddress && maxRadius) {
        userLatLng = getLatLngViaHttpRequest(userAddress);
    }

    function getLatLngViaHttpRequest(address) {
        // Set up a request to the Geocoding API
        // Supported address format is City, City + State, just a street address, or any combo
        var addressStripped = address.split(' ').join('+');
        var key = "AIzaSyBdRX49meltvAx46ktO4zUqkP1I_ZHBgF4";
        var request = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + addressStripped + '&key=' + key;

        // Call the Geocoding API using jQuery GET, passing in the request and a callback function
        // which takes one argument "data" containing the response
        $.get( request, function( data ) {
            var searchResultsAlert = document.getElementById('location-search-alert');

            // Abort if there is no response for the address data
            if (data.status === "ZERO_RESULTS") {
                searchResultsAlert.innerHTML = "Sorry, '" + address + "' seems to be an invalid address.";
                return;
            }

            var userLatLng = new google.maps.LatLng(data.results[0].geometry.location.lat, data.results[0].geometry.location.lng);
            var filteredLocations = stylists.filter(isWithinRadius);

            if (filteredLocations.length > 0) {
                createSearchableMap(filteredLocations);
                createListOfLocations(filteredLocations);
                searchResultsAlert.innerHTML = 'Stylist within ' + maxRadius + ' miles of ' + userAddress + ':';
            } else {
                console.log("nothing found!");
                document.getElementById('locations-near-you').innerHTML = '';
                searchResultsAlert.innerHTML = 'Sorry, no stylist were found within '+ maxRadius + ' miles of ' + userAddress + '.';
            }

            function isWithinRadius(location) {
                var locationLatLng = new google.maps.LatLng(location.lat, location.lng);
                var distanceBetween = google.maps.geometry.spherical.computeDistanceBetween(locationLatLng, userLatLng);

                return convertMetersToMiles(distanceBetween) <= maxRadius;
            }
        });
    }
}
function convertMetersToMiles(meters) {
    return (meters * 0.000621371);
}

function createListOfLocations(locations) {
    var locationsList = document.getElementById('stylists-near-you');

    // Clear any existing locations from the previous search first
    locationsList.innerHTML = '';

    locations.forEach( function(location) {
        var specificLocation = document.createElement('div');
        var locationInfo =  location.fields.businessname + location.fields.address  +
            location.fields.city + location.fields.state + location.fields.zip;
        specificLocation.setAttribute("class", 'location-near-you-box');
        specificLocation.innerHTML = locationInfo;
        locationsList.appendChild(specificLocation);
    });
}
$('#submitLocationSearch').on('click', function(e) {
    e.preventDefault();
    filterLocations();
});

new google.maps.LatLng(data.results[0].geometry.location.lat, data.results[0].geometry.location.lng)