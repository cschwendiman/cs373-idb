angular.module('directives', [])
    .directive('showTable', function() {
        return {
            restrict: 'A',
            scope: false,
            link: function(scope, element, attrs) {
                scope.tableOn = false;
                element.bind('click', function() {
                    scope.$apply(function() {
                        scope.tableOn = (attrs.showTable === "on");
                    });
                });
                scope.$watch('tableOn', function(newValue, oldValue) {
                    if (newValue != oldValue) {
                        element.toggleClass("active");
                    }
                })
            }
        };
    });