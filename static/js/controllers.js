angular.module('controllers', [])
    .controller('IndexController', function () {
        mapWrapper.init();
    })
    .controller('MainController', function ($scope, tweets, hashtags, locations) {
        twttr.ready(function () {
            tweets.length = 6;
            $scope.$tweets = tweets;
            for (var i = 0; i < tweets.length; i++) {
                twttr.widgets.createTweet(
                    tweets[i].twitter_tweet_id,
                    document.getElementById('recent-tweets'),
                    {align: 'left'});
            }
            hashtags.length = 10;
            $scope.$hashtags = hashtags;
            $scope.$locations = locations;
        });
        mapWrapper.clearMarkers();
    })
    .controller('AboutController', function ($http) {
        var runtestsbtn = $('#run-tests');
        runtestsbtn.bind('click', function() {
            $('#test-results').remove();
            $http.get("/unit-tests/")
                .success(function(response) {
                    runtestsbtn.after("<pre id='test-results'>" + response + "</pre>");
                });

        })
    })
    .controller('TweetsController', function ($scope, tweets) {
        tweets.length = 30;
        $scope.$tweets = tweets;
        mapWrapper.addTweets(tweets);
    })
    .controller('TweetController', function ($scope, tweet, hashtags, Location) {
        mapWrapper.clearMarkers();
        mapWrapper.addTweet(tweet);
        mapWrapper.setBounds();
        $scope.$tweet = tweet;
        twttr.ready(function () {
            twttr.widgets.createTweet(
                tweet.twitter_tweet_id,
                document.getElementById('tweet-container'),
                {align: 'left'});
        });

        Location.get({id: tweet.city_id}, function (city) {
            $scope.$tweet.location = city;
        });

        $scope.$tweet.hashtags = hashtags;
    })
    .controller('HashtagsController', function ($scope, $q, hashtags, Hashtag) {
        hashtags.length = 40;
        $scope.$hashtags = hashtags;

        var tweets = {};
        var promises = [];
        for (var i = 0; i < hashtags.length; i++) {
            var hashtag = $scope.$hashtags[i];
            var future_tweets = Hashtag.tweets({id: hashtag.id}, function (data) {
                if (data.length > 10) {
                    data.length = 10;
                }
                for (var i = 0; i < data.length; i++) {
                    var tweet = data[i];
                    if (!tweets[tweet.id]) {
                        tweets[tweet.id] = tweet;
                        tweets[tweet.id].hashtags = [];
                    }
                    tweets[tweet.id].hashtags.push(hashtag);
                }
            });
            promises.push(future_tweets.$promise);
        }
        $q.all(promises).then(function () {
            mapWrapper.addHashtags(tweets);
        })
    })
    .controller('HashtagController', function ($scope, hashtag, tweets, locations) {
        $scope.$hashtag = hashtag;

        if (tweets.length > 10) {
            tweets.length = 10;
        }
        $scope.$hashtag.tweets = tweets;
        mapWrapper.addTweets(tweets);
        twttr.ready(function () {
            for (var i = 0; i < tweets.length; i++) {
                twttr.widgets.createTweet(
                    tweets[i].twitter_tweet_id,
                    document.getElementById('tweet-container'),
                    {align: 'left'});
            }
        });

        $scope.$hashtag.locations = locations;

    })
    .controller('LocationsController', function ($scope, locations) {
        $scope.$locations = locations;
        mapWrapper.clearMarkers();
        var gc = new google.maps.Geocoder();
        for (var i = 0; i < locations.length; i++) {
            (function (location) {
                var address = location.city + ", " + location.state + ", " + location.country;
                gc.geocode({address: address}, function (r, s) {
                    mapWrapper.addLocation(location, r[0].geometry.location);
                });
            })(locations[i]);
        }

    })
    .controller('LocationController', function ($scope, location, hashtags, tweets) {
        $scope.$location = location;

        if (tweets.length > 10) {
            tweets.length = 10;
        }
        $scope.$location.tweets = tweets;
        mapWrapper.addTweets(tweets);
        var tweet_ids = tweets.map(function (tweet) {
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

        hashtags.length = 10;
        $scope.$location.hashtags = hashtags;
    })
    .controller('SearchController', function ($scope, $location, $http) {
        $http.get("/api/search/" + $location.search().q)
            .success(function(response) {
                $scope.$and_tweets = response.tweets;
                $scope.$or_tweets = response.tweets_or;
                $scope.$and_hashtags = response.hashtags;
                $scope.$or_hashtags = response.hashtags_or;
        });

    });