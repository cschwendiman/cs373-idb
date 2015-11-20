angular.module('api', [])
    .config(['$resourceProvider', function ($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs because they cause redirects
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }])
    .factory('Tweet', function ($resource) {
        return $resource('/api/tweets/:id/', {}, {
            query: {method: 'GET', params: {}, isArray: true, url: '/api/tweets/pages/:page/'},
            hashtags: {method: 'GET', isArray: true, url: '/api/tweets/:id/hashtags/'}
        });
    })
    .factory('Hashtag', function ($resource) {
        return $resource('/api/hashtags/:id/', {}, {
            query: {method: 'GET', params: {}, isArray: true, url: '/api/hashtags/'},
            tweets: {method: 'GET', isArray: true, url: '/api/hashtags/:id/tweets/'},
            locations: {method: 'GET', isArray: true, url: '/api/hashtags/:id/cities/'}
        });
    })
    .factory('Location', function ($resource) {
        return $resource('/api/locations/:id/', {}, {
            query: {method: 'GET', params: {}, isArray: true, url: '/api/locations/'},
            tweets: {method: 'GET', isArray: true, url: '/api/locations/:id/tweets/'},
            hashtags: {method: 'GET', isArray: true, url: '/api/locations/:id/hashtags/'}
        });
    });