angular.module('api', [])
    .config(['$resourceProvider', function($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs because they cause redirects
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }])
    .factory('Tweet', function($resource){
        return $resource('/api/tweet/:id/', {}, {
            query: {method: 'GET', params: {}, isArray: true, url: '/api/tweets/'},
            hashtags: {method: 'GET', isArray:true, url: '/api/hashtagsByTweet/:id/'}
        });
    })
    .factory('Hashtag', function($resource) {
        return $resource('/api/hashtag/:id/', {}, {
            query: {method: 'GET', params: {}, isArray: true, url: '/api/hashtags/'},
            tweets: {method: 'GET', isArray:true, url: '/api/tweetsByHashtag/:id/'},
            locations: {method: 'GET', isArray:true, url: '/api/locationsByHashtag/:id/'}
        });
    })
    .factory('Location', function($resource) {
        return $resource('/api/location/:id/', {}, {
            query: {method: 'GET', params: {}, isArray: true, url: '/api/locations/'},
            tweets: {method: 'GET', isArray:true, url: '/api/tweetsByCity/:id/'},
            hashtags: {method: 'GET', isArray:true, url: '/api/hashtagsByCity/:id/'}
        });
    });