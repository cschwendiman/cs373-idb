angular.module('tweetcity', ['ngRoute', 'ngResource', 'api', 'controllers'])
    .config(function ($routeProvider, $locationProvider) {
        $routeProvider
            .when('/', {
                title: "",
                templateUrl: '/static/templates/main.html',
                controller: 'MainController'
            })
            .when('/about', {
                title: "About",
                templateUrl: '/static/templates/about.html',
                controller: 'AboutController'
            })
            .when('/hashtags', {
                title: "Hashtags",
                templateUrl: '/static/templates/hashtags.html',
                controller: 'HashtagsController'
            })
            .when('/hashtag/:id', {
                title: "Hashtag",
                templateUrl: '/static/templates/hashtag.html',
                controller: 'HashtagController'
            })
            .when('/locations', {
                title: "Locations",
                templateUrl: '/static/templates/locations.html',
                controller: 'LocationsController'
            })
            .when('/location/:id', {
                title: "Location",
                templateUrl: '/static/templates/location.html',
                controller: 'LocationController'
            })
            .when('/tweets', {
                title: "Tweets",
                templateUrl: '/static/templates/tweets.html',
                controller: 'TweetsController'
            })
            .when('/tweet/:id', {
                title: "Tweet",
                templateUrl: '/static/templates/tweet.html',
                controller: 'TweetController'
            })
            .otherwise({redirectTo: '/'});
        $locationProvider.html5Mode(true);
    })
    .run(['$rootScope', function ($rootScope) {
        $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
            $rootScope.title = current.$$route.title;

        });
    }]);