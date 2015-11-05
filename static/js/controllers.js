angular.module('controllers', [])
    .controller('IndexController', function ($scope, Tweet, Hashtag, Location) {
        Tweet.query(function(data) {
            $scope.$tweets = data.tweets;
        });
        Hashtag.query(function(data) {
            $scope.$hashtags = data.hashtags;
        });
        Location.query(function(data) {
            $scope.$locations = data.locations;
        });
        mapWrapper.init();
    })
    .controller('MainController', function ($scope) {
        twttr.ready(function () {
            for (i in $scope.$tweets) {
                twttr.widgets.createTweet(
                    $scope.$tweets[i].tweet_id,
                    document.getElementById('recent-tweets'),
                    {align: 'left'});
            }
        });
        $('#jumbo-header').slideDown("slow");
        mapWrapper.clearMarkers();
    })
    .controller('AboutController', function ($scope) {
        $('#jumbo-header').slideUp("slow");
    })
    .controller('TweetsController', function($scope, Tweet) {
        /*
        var tweet = Tweet.get({id: $scope.id}, function() {
            console.log(tweet);
        });
        var tweets = Tweet.query(function() {
            console.log(tweets);
        })
        */
        $(document).ready(function(){
        $("#tweets-table").tablesorter();
        });
        $('#jumbo-header').slideDown("slow");
        mapWrapper.addTweets($scope.$tweets);
    })
    .controller('TweetController', function ($scope, $routeParams) {
        var tweet = $scope.$tweets[$routeParams.id];
        $scope.tweet = tweet;
        if (tweet) {
            twttr.ready(function () {
                twttr.widgets.createTweet(
                    tweet.tweet_id,
                    document.getElementById('tweet-container'),
                    {align: 'left'});
            });
        }
        $('#jumbo-header').slideDown("slow");
    })
    .controller('HashtagsController', function($scope, Hashtag) {
        /*
        var hashtag = Hashtag.get({id: $scope.id}, function() {
            console.log(hashtag);
        });
        var hashtags = Hashtag.query(function() {
            console.log(hashtags);
        })*/
        var hashtags = $scope.$hashtags;
        var tweets = $scope.$tweets;
        angular.forEach(tweets, function(tweet, id) {
            tweet.full_hashtags = [];
            for (var i = 0; i < tweets[id].hashtags.length; i++) {
                tweets[id].full_hashtags.push(hashtags[tweets[id].hashtags[i]]);
            }
        });
        $('#jumbo-header').slideDown("slow");
        mapWrapper.addHashtags(tweets);
    })
    .controller('HashtagController', function ($scope, $routeParams) {
        var hashtag = $scope.$hashtags[$routeParams.id];
        $scope.hashtag = hashtag;
        var tweet_ids = hashtag.tweets.map(function (id) {
            return $scope.$tweets[id].tweet_id
        });
        twttr.ready(function () {
            for (var i = 0; i < tweet_ids.length; i++) {
                twttr.widgets.createTweet(
                    tweet_ids[i],
                    document.getElementById('tweet-container'),
                    {align: 'left'});
            }
        });
        $('#jumbo-header').slideDown("slow");

    })
    .controller('LocationsController', function($scope, Location) {
        /*
        var location = Location.get({id: $scope.id}, function() {
            console.log(location);
        });
        var locations = Location.query(function() {
            console.log(locations);
        })
        */
        $('#jumbo-header').slideDown("slow");
        mapWrapper.clearMarkers();
        var gc = new google.maps.Geocoder();
        for (i in $scope.$locations) {
            var location = $scope.$locations[i];
            var address = location.city + ", " + location.state + ", " + location.country;
            gc.geocode({address: address}, function (r, s) {
                mapWrapper.addLocation(location, r[0].geometry.location);
            })
        }
    })
    .controller('LocationController', function ($scope, $routeParams) {
        var location = $scope.$locations[$routeParams.id];
        $scope.location = location;
        var tweet_ids = location.tweets.map(function (id) {
            return $scope.$tweets[id].tweet_id
        });
        twttr.ready(function () {
            for (var i = 0; i < tweet_ids.length; i++) {
                twttr.widgets.createTweet(
                    tweet_ids[i],
                    document.getElementById('tweet-container'),
                    {align: 'left'});
            }
        });
        $('#jumbo-header').slideDown("slow");
    });