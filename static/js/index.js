angular.module('tweetcity', ['ngRoute', 'ngResource', 'api', 'controllers', 'directives', 'angularUtils.directives.dirPagination'])
    .config(function ($routeProvider, $locationProvider) {
        $routeProvider
            .when('/', {
                title: "",
                templateUrl: '/static/templates/main.html',
                controller: 'MainController',
                resolve: {
                    tweets: function (Tweet) {
                        return Tweet.query({page: 1}).$promise;
                    },
                    hashtags: function (Hashtag) {
                        return Hashtag.query({page: 1}).$promise;
                    },
                    locations: function (Location) {
                        return Location.query({page: 1}).$promise;
                    }
                }
            })
            .when('/about', {
                title: "About",
                templateUrl: '/static/templates/about.html',
                controller: 'AboutController'
            })
            .when('/hashtags', {
                title: "Hashtags",
                templateUrl: '/static/templates/hashtags.html',
                controller: 'HashtagsController',
                resolve: {
                    hashtags: function (Hashtag) {
                        return Hashtag.query({page: 1}).$promise;
                    }
                }
            })
            .when('/hashtags/:id', {
                title: "Hashtag",
                templateUrl: '/static/templates/hashtag.html',
                controller: 'HashtagController',
                resolve: {
                    hashtag: function (Hashtag, $route) {
                        return Hashtag.get({id: $route.current.params.id}).$promise;
                    },
                    locations: function (Hashtag, $route) {
                        return Hashtag.locations({id: $route.current.params.id}).$promise;
                    },
                    tweets: function (Hashtag, $route) {
                        return Hashtag.tweets({id: $route.current.params.id}).$promise;
                    }
                }
            })
            .when('/locations', {
                title: "Locations",
                templateUrl: '/static/templates/locations.html',
                controller: 'LocationsController',
                resolve: {
                    locations: function (Location) {
                        return Location.query({page: 1}).$promise;
                    }
                }
            })
            .when('/locations/:id', {
                title: "Location",
                templateUrl: '/static/templates/location.html',
                controller: 'LocationController',
                resolve: {
                    location: function (Location, $route) {
                        return Location.get({id: $route.current.params.id}).$promise;
                    },
                    hashtags: function (Location, $route) {
                        return Location.hashtags({id: $route.current.params.id}).$promise;
                    },
                    tweets: function (Location, $route) {
                        return Location.tweets({id: $route.current.params.id}).$promise;
                    }
                }
            })
            .when('/tweets', {
                title: "Tweets",
                templateUrl: '/static/templates/tweets.html',
                controller: 'TweetsController',
                resolve: {
                    tweets: function (Tweet) {
                        return Tweet.query({page: 1}).$promise;
                    }
                }
            })
            .when('/tweets/:id', {
                title: "Tweet",
                templateUrl: '/static/templates/tweet.html',
                controller: 'TweetController',
                resolve: {
                    tweet: function (Tweet, $route) {
                        return Tweet.get({id: $route.current.params.id}).$promise;
                    },
                    hashtags: function (Tweet, $route) {
                        return Tweet.hashtags({id: $route.current.params.id}).$promise;
                    }
                }
            })
            .when('/search', {
                title: "Search Results",
                templateUrl: '/static/templates/search.html',
                controller: 'SearchController'
            })
            .when('/animedb', {
                title: "AnimeDB Search",
                templateUrl: '/static/templates/animedb.html',
                controller: 'AnimeDBController'
            })
            .otherwise({redirectTo: '/'});
        $locationProvider.html5Mode(true);
    })
    .run(['$rootScope', function ($rootScope) {
        $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
            $rootScope.title = current.$$route.title;

        });
    }]);