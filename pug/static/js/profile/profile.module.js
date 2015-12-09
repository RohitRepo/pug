angular.module("ProfileApp", ["module.root", "ui.router"])
.value('$anchorScroll', angular.noop)
.config(['$httpProvider',
    '$interpolateProvider',
    '$locationProvider',
    '$stateProvider',
    '$urlRouterProvider',
    function ($httpProvider,
        $interpolateProvider,
        $locationProvider,
        $stateProvider,
        $urlRouterProvider) {
    "use strict";

    // Changing angular template tag to prevent conflict with django
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]')

    // csrf for django
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';

    // For any unmatched url, reload as we have not mentioned any base
    $urlRouterProvider.otherwise(
        function() {
            window.location.reload();

    });

    // use the HTML5 History API
    $locationProvider.html5Mode(true);

    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/devices");
    //
    // Now set up the states
    $stateProvider
    .state('devices', {
        url: "/devices",
        templateUrl: "/static/js/profile/profile.devices.html",
        controller: 'profileDevicesController'
    })
    .state('add', {
        url: "/new-device",
        templateUrl: "/static/js/profile/profile.add.html",
        controller: 'profileAddController'
    });
}]);