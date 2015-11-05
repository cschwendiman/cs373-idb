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
        for (tweet_id in tweets) {
            this.addHashtag(tweets[tweet_id]);
        }
        this.setBounds();
    },
    addHashtag: function (tweet) {
        var links = "";
        for (var i = 0; i < tweet.full_hashtags.length; i++) {
            links += ' <a href="/hashtag/' + tweet.full_hashtags[i].id + '">' + tweet.full_hashtags[i].name + '</a>';
        }
        var infowindow = new google.maps.InfoWindow({
            content: links
        });
        var marker = new google.maps.Marker({
            position: {lat: tweet.latitude, lng: tweet.longitude},
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
        var id;
        for (id in tweets) {
            this.addTweet(tweets[id]);
        }
        this.setBounds();
    },
    addTweet: function (tweet) {
        var link = tweet.text + ' <a href="/tweet/' + tweet.id + '">See more details</a>';
        var infowindow = new google.maps.InfoWindow({
            content: link
        });

        var marker = new google.maps.Marker({
            position: {lat: tweet.latitude, lng: tweet.longitude},
            map: this.map,
            title: tweet.name
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