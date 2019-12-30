


// document.querySelector('#use-location').addEventListener('click', Locator);

function initMap() {

    function Locator() {
        // console.log(latitude, longitude);

        const status = document.querySelector('#status');
        const mapLink = document.querySelector('#map-link');

        mapLink.href = '';
        mapLink.textContent = '';

        function success(position) {
            let latitude  = position.coords.latitude;
            let longitude = position.coords.longitude;
            console.log(latitude, longitude);

            fetch("/update_location/", {
                method: "PUT",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    latitude: latitude,
                    longitude: longitude,
                })
            })
                .then(data => data.text())

                .then(info=> {
                    console.log(info)
                });


            status.textContent = '';
            // The location of Uluru
            let uluru = {lat: latitude, lng: longitude};
            // The map, centered at Uluru
            let map = new google.maps.Map(
                document.getElementById('map'), {zoom: 6, center: uluru});
            // The marker, positioned at Uluru
            let marker = new google.maps.Marker({position: uluru, map: map});



            // mapLink.href = `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`;
            // mapLink.textContent = `Latitude: ${latitude} °, Longitude: ${longitude} °`;
        }

        function error() {
            status.textContent = 'Unable to retrieve your location';
        }

        if (!navigator.geolocation) {
            status.textContent = 'Geolocation is not supported by your browser';
        } else {
            status.textContent = 'Locating…';
            navigator.geolocation.getCurrentPosition(success, error);
        }

    }

    // The location of Uluru
    let uluru = {lat: 0, lng: 0};
    // The map, centered at Uluru
    let map = new google.maps.Map(
        document.getElementById('map'), {zoom: 6, center: uluru});
    // The marker, positioned at Uluru
    let marker = new google.maps.Marker({position: uluru, map: map});

    document.querySelector('#use-location').addEventListener('click', Locator);
}
