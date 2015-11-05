angular.module('api', [])
    .factory('Tweet', function($resource){
        /*
        return $resource('/api/tweet/:id', {}, {
            query: {method: 'GET', params: {}, isArray: true, url: '/api/tweets' }
        });
        */
        return $resource('/static/json/tweets.json');
    })
    .factory('Hashtag', function($resource) {
        /*
        return $resource('/api/hashtag/:id', {}, {
            query: {method: 'GET', params: {}, isArray: true, url: '/api/hashtags' }
        });
        */
        return $resource('/static/json/hashtags.json');
    })
    .factory('Location', function($resource) {
        /*
        return $resource('/api/location/:id', {}, {
            query: {method: 'GET', params: {}, isArray: true, url: '/api/locations' }
        });
        */
        return $resource('/static/json/locations.json');
    });