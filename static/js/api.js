angular.module('api', [])
    .config(['$resourceProvider', function($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs because they cause redirects
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }])
    .factory('Tweet', function($resource){
        return $resource('/api/tweet/:id/', {}, {
            query: {method: 'GET', params: {}, isArray: true, url: '/api/tweets/'},
            hashtags: {method: 'GET', isArray:true, url: '/api/tweet/:id/hashtags/'}
        });
    })
    .factory('Hashtag', function($resource) {
        return $resource('/api/hashtag/:id/', {}, {
            query: {method: 'GET', params: {}, isArray: true, url: '/api/hashtags/'},
            tweets: {method: 'GET', isArray:true, url: '/api/hashtag/:id/tweets/'},
            locations: {method: 'GET', isArray:true, url: '/api/hashtag/:id/cities/'}
        });
    })
    .factory('Location', function($resource) {
        return $resource('/api/location/:id/', {}, {
            query: {method: 'GET', params: {}, isArray: true, url: '/api/locations/'},
            tweets: {method: 'GET', isArray:true, url: '/api/location/:id/tweets/'},
            hashtags: {method: 'GET', isArray:true, url: '/api/location/:id/hashtags/'}
        });
    });