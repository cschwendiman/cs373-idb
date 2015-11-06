var mapWrapper = {
    map: null,
    ele: "map",
    markers: [],
    options: {
        zoomControl: false,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        center: {lat: 30.25, lng: -97.75},
        zoom: 10
    },
    init: function () {
        if (this.map == null) {
            this.map = new google.maps.Map(document.getElementById('map'), this.options);
        }
    },
    addHashtags: function (tweets) {
        this.clearMarkers();
        for (var i in tweets) {
            this.addHashtag(tweets[i]);
        }
        this.setBounds();
    },
    addHashtag: function (tweet) {
        var links = "";
        for (var i = 0; i < tweet.hashtags.length; i++) {
            links += ' <a href="/hashtag/' + tweet.hashtags[i].id + '">#' + tweet.hashtags[i].text + '</a>';
        }
        var infowindow = new google.maps.InfoWindow({
            content: links
        });
        var marker = new google.maps.Marker({
            position: {lat: tweet.longitude, lng: tweet.latitude},
            map: this.map,
            title: "Hashtags"
        });
        this.markers.push(marker);
        marker.addListener('click', function () {
            infowindow.open(this.map, marker);
        });
    },
    addLocation: function (location, coords) {
        var link = location.city + ', ' + location.state + ' <a href="/location/' + location.id + '">See more details</a>';
        var infowindow = new google.maps.InfoWindow({
            content: link
        });

        var marker = new google.maps.Marker({
            position: coords,
            map: this.map,
            title: location.name
        });
        this.markers.push(marker);
        marker.addListener('click', function () {
            infowindow.open(this.map, marker);
        });
        this.setBounds();
    },
    addTweets: function (tweets) {
        this.clearMarkers();
        console.log("hi");
        console.log(tweets);
        for (var i = 0; i < tweets.length; i++) {
            this.addTweet(tweets[i]);
        }
        this.setBounds();
    },
    addTweet: function (tweet) {
        var link = tweet.text + ' <a href="/tweet/' + tweet.id + '">See more details</a>';
        var infowindow = new google.maps.InfoWindow({
            content: link
        });

        var marker = new google.maps.Marker({
            position: {lat: tweet.longitude, lng: tweet.latitude},
            map: this.map,
            title: "Tweet " + tweet.id
        });
        this.markers.push(marker);
        marker.addListener('click', function () {
            infowindow.open(this.map, marker);
        });
    },
    setBounds: function () {
        var bounds = new google.maps.LatLngBounds();
        for (i = 0; i < this.markers.length; i++) {
            bounds.extend(this.markers[i].getPosition());
        }
        google.maps.event.addListener(map, 'bounds_changed', function () {
            this.map.setCenter(bounds.getCenter());
        });
        this.map.fitBounds(bounds);
    },
    clearMarkers: function () {
        for (var i = 0; i < this.markers.length; i++) {
            this.markers[i].setMap(null);
        }
        this.markers.length = 0;
        this.map.setCenter({lat: 30.25, lng: -97.75});
    }
};