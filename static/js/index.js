console.log("load");


angular.module('tweetcity', ['ngRoute'])

    .controller('IndexController', function ($scope, $route, $routeParams, $location) {
        $scope.$route = $route;
        $scope.$location = $location;
        $scope.$routeParams = $routeParams;
        $scope.$routeParams.title = "";
        $scope.$hashtags = {
            1: {
                id: 1,
                name: '#austin',
                locations: [1, 2],
                tweets: [2, 3]
            },
            2: {
                id: 2,
                name: '#texas',
                locations: [1, 2],
                tweets: [1, 2]
            },
            3: {
                id: 3,
                name: '#wedding',
                locations: [1, 2],
                tweets: [3, 4]
            }
        };
        $scope.$locations = {
            1: {
                id: 1,
                city: "Austin",
                state: "TX",
                country: "US",
                tweets: [2, 3],
                hashtags: [1, 2, 3]
            },
            2: {
                id: 2,
                city: "Round Rock",
                state: "TX",
                country: "US",
                tweets: [1, 4],
                hashtags: [2, 3]
            }
        };
        $scope.$tweets = {
            1: {
                id: 1,
                text: "#Beautiful #Texas #sunset. #ontheroadagain @ Round Rock, Texas https://t.co/Q3gYPffqGz",
                username: "tinocrane68",
                location: 2,
                url: '',
                longitude: 30.5149,
                latitude: -97.6726,
                hashtags: [2],
                tweet_id: '655538544182718465'
            },
            2: {
                id: 2,
                text: "can't stop eating #queso I need to leave #austin #texas follow my adventures in #snapchat \u2600\ufe0f\ud83c\udf35\ud83d\udc62\ud83d\udc52 @ The\u2026 https://t.co/g1RROokrMd",
                username: "kiraklapper",
                location: 1,
                url: '',
                longitude: 30.2641201,
                latitude: -97.7426529,
                hashtags: [1, 2],
                tweet_id: '655477025608589312'
            },
            3: {
                id: 3,
                text: "Seafood #icesculpture display with #monogram for s lovely #wedding on this gorgeous #austin night\u2026 https://t.co/dTBuwz75FR",
                username: "fullspectrumice",
                location: 1,
                url: '',
                longitude: 30.2831802,
                latitude: -97.7455063,
                hashtags: [1, 3],
                tweet_id: '655558187005837312'
            },
            4: {
                id: 4,
                text: "From #wedding receptions to #homecoming dances we do it all! Set up at the beautiful Inn at Wild Rose\u2026 https://t.co/HOsbJEh2Gl",
                username: "austincityphoto",
                location: 2,
                url: '',
                longitude: 30.4925,
                latitude: -97.64027778,
                hashtags: [3],
                tweet_id: '655532129380638720'
            }
        }
    })

    .controller('MainController', function ($scope, $routeParams) {
        $scope.name = "MainController";
        $scope.params = $routeParams;
    })

    .controller('AboutController', function ($scope, $routeParams) {
        $scope.name = "AboutController";
        $scope.params = $routeParams;
    })

    .controller('HashtagsController', function ($scope, $routeParams) {
        $scope.name = "HashtagsController";
        $scope.params = $routeParams;
    })

    .controller('HashtagController', function ($scope, $routeParams) {
        $scope.name = "HashtagController";
        $scope.params = $routeParams;
        var hashtag = $scope.$hashtags[$routeParams.id];
        $scope.hashtag = hashtag;
        var tweet_ids = hashtag.tweets.map(function(id){
            return $scope.$tweets[id].tweet_id
        });
        twttr.ready(function(){
            for (var i = 0; i < tweet_ids.length; i++) {
                twttr.widgets.createTweet(
                    tweet_ids[i],
                    document.getElementById('tweet-container'),
                    {align: 'left'});
            }
        });
    })

    .controller('LocationsController', function ($scope, $routeParams) {
        $scope.name = "LocationsController";
        $scope.params = $routeParams;
    })

    .controller('LocationController', function ($scope, $routeParams) {
        $scope.name = "LocationController";
        $scope.params = $routeParams;
        var location = $scope.$locations[$routeParams.id];
        $scope.location = location;
        var tweet_ids = location.tweets.map(function(id){
            return $scope.$tweets[id].tweet_id
        });
        twttr.ready(function(){
            for (var i = 0; i < tweet_ids.length; i++) {
                twttr.widgets.createTweet(
                    tweet_ids[i],
                    document.getElementById('tweet-container'),
                    {align: 'left'});
            }
        });
    })

    .controller('TweetsController', function ($scope, $routeParams) {
        $scope.name = "TweetsController";
        $scope.params = $routeParams;
    })

    .controller('TweetController', function ($scope, $routeParams) {
        $scope.name = "TweetController";
        $scope.params = $routeParams;
        var tweet = $scope.$tweets[$routeParams.id];
        $scope.tweet = tweet;
        twttr.ready(function(){
            twttr.widgets.createTweet(
                tweet.tweet_id,
                document.getElementById('tweet-container'),
                {align: 'left'});
        });
    })

    .config(function ($routeProvider, $locationProvider) {
        $routeProvider
            .when('/', {
                title: "",
                templateUrl: '/static/main.html',
                controller: 'MainController'
            })
            .when('/about', {
                title: "About",
                templateUrl: '/static/about.html',
                controller: 'TweetController'
            })
            .when('/hashtags', {
                title: "Hashtags",
                templateUrl: '/static/hashtags.html',
                controller: 'HashtagsController'
            })
            .when('/hashtag/:id', {
                title: "Hashtag",
                templateUrl: '/static/hashtag.html',
                controller: 'HashtagController'
            })
            .when('/locations', {
                title: "Locations",
                templateUrl: '/static/locations.html',
                controller: 'LocationsController'
            })
            .when('/location/:id', {
                title: "Location",
                templateUrl: '/static/location.html',
                controller: 'LocationController'
            })
            .when('/tweets', {
                title: "Tweets",
                templateUrl: '/static/tweets.html',
                controller: 'TweetsController'
            })
            .when('/tweet/:id', {
                title: "Tweet",
                templateUrl: '/static/tweet.html',
                controller: 'TweetController'
            })
            .otherwise({ redirectTo: '/' });
        $locationProvider.html5Mode(true);
    })

.run(['$rootScope', function($rootScope) {
    $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
        $rootScope.title = current.$$route.title;

    });
}]);