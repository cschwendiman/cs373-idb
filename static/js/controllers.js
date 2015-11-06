angular.module('controllers', [])
    .controller('IndexController', function () {
        mapWrapper.init();
    })
    .controller('MainController', function ($scope, Tweet, Hashtag, Location) {
        twttr.ready(function () {
            Tweet.query(function(data) {
                data.length = 6;
                $scope.$tweets = data;
                for (var i = 0; i < data.length; i++) {
                twttr.widgets.createTweet(
                    $scope.$tweets[i].twitter_tweet_id,
                    document.getElementById('recent-tweets'),
                    {align: 'left'});
            }
            });
            Hashtag.query(function(data) {
                data.length = 10;
                $scope.$hashtags = data;
            });
            Location.query(function(data) {
                $scope.$locations = data;
            });
        });
        $('#jumbo-header').slideDown("slow");
        mapWrapper.clearMarkers();
    })
    .controller('AboutController', function () {
        $('#jumbo-header').slideUp("slow");
    })
    .controller('TweetsController', function($scope, Tweet) {
        Tweet.query(function(data) {
            data.length = 20;
            $scope.$tweets = data;
            console.log(data);
            mapWrapper.addTweets($scope.$tweets);
        });
        $('#jumbo-header').slideDown("slow");
    })
    .controller('TweetController', function ($scope, $routeParams, Tweet, Location) {
        Tweet.get({id: $routeParams.id}, function(data) {
            $scope.$tweet = data;
            if (data) {
                twttr.ready(function () {
                    twttr.widgets.createTweet(
                        data.twitter_tweet_id,
                        document.getElementById('tweet-container'),
                        {align: 'left'});
                });
                Location.get({id: data.city_id}, function(city) {
                    $scope.$tweet.location = city;
                });
                Tweet.hashtags({id: data.id}, function(hashtags) {
                    $scope.$tweet.hashtags = hashtags;
                });
            }
        });
        $('#jumbo-header').slideDown("slow");
    })
    .controller('HashtagsController', function($scope, Hashtag) {
        Hashtag.query(function(data) {
            var tweets = {};
            data.length = 20;
            $scope.$hashtags = data;
            for (var i = 0; i < data.length; i++) {
                var hashtag = $scope.$hashtags[i];
                Hashtag.tweets({id: hashtag.id}, function(data) {
                    if(data.length > 10) {
                        data.length = 10;
                    }
                    for (var i = 0; i < data.length; i++) {
                        var tweet = data[i];
                        console.log(tweet);
                        if (! tweets[tweet.id]) {
                            tweets[tweet.id] = tweet;
                            tweets[tweet.id].hashtags = [];
                        }
                        tweets[tweet.id].hashtags.push(hashtag);
                    }
                });
            }
            console.log(tweets);
            mapWrapper.addHashtags(tweets);
        });
        $('#jumbo-header').slideDown("slow");

    })
    .controller('HashtagController', function ($scope, $routeParams, Hashtag) {
        Hashtag.get({id: $routeParams.id}, function(data) {
            $scope.$hashtag = data;

            Hashtag.tweets({id: $scope.$hashtag.id}, function(data) {
                if (data.length > 10) {
                    data.length = 10;
                }
                $scope.$hashtag.tweets = data;
                twttr.ready(function () {
                    for (var i = 0; i < data.length; i++) {
                        twttr.widgets.createTweet(
                            data[i].twitter_tweet_id,
                            document.getElementById('tweet-container'),
                            {align: 'left'});
                    }
                });
            });

            Hashtag.locations({id: $scope.$hashtag.id}, function(data) {
                $scope.$hashtag.locations = data;
            })
        });
        $('#jumbo-header').slideDown("slow");

    })
    .controller('LocationsController', function($scope, Location) {
        Location.query(function(data) {
            $scope.$locations = data;
            mapWrapper.clearMarkers();
            var gc = new google.maps.Geocoder();
            for (var i = 0; i < $scope.$locations.length; i++) {
                (function(location){
                    var address = location.city + ", " + location.state + ", " + location.country;
                    gc.geocode({address: address}, function (r, s) {
                        console.log(r);
                        console.log(location);
                        mapWrapper.addLocation(location, r[0].geometry.location);
                    });
                })($scope.$locations[i]);

            }
        });
        $('#jumbo-header').slideDown("slow");

    })
    .controller('LocationController', function ($scope, $routeParams, Location) {
        Location.get({id: $routeParams.id}, function(data) {
            $scope.$location = data;
            Location.tweets({id: $scope.$location.id}, function(data) {
                data.length = 10;
                $scope.$location.tweets = data;
                var tweet_ids = data.map(function (tweet) {
                    return tweet.twitter_tweet_id
                });
                twttr.ready(function () {
                for (var i = 0; i < tweet_ids.length; i++) {
                    twttr.widgets.createTweet(
                        tweet_ids[i],
                        document.getElementById('tweet-container'),
                        {align: 'left'});
                    }
                });
            });
            Location.hashtags({id: $scope.$location.id}, function(data) {
                data.length = 10;
                console.log(data);
                $scope.$location.hashtags = data;
            });
        });
        $('#jumbo-header').slideDown("slow");
    });