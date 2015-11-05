angular.module('api', [])
    .factory('Tweet', function($resource){
        return $resource('/api/tweet/:id', {}, {
            query: {method: 'GET', params: {}, isArray: false, url: '/api/tweets' }
        });
    })
    .factory('Hashtag', function($resource) {
        return $resource('/api/hashtag/:id', {}, {
            query: {method: 'GET', params: {}, isArray: false, url: '/api/hashtags' }
        });
    })
    .factory('Location', function($resource) {
        return $resource('/api/location/:id', {}, {
            query: {method: 'GET', params: {}, isArray: false, url: '/api/locations' }
        });
    });