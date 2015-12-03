angular.module("module.model")
.factory("userModel", ['$http', '$q', function ($http, $q) {
    var service = {};

    var baseUrl = '/api/v1/users/'

    service.login = function (email, password) {
        return $http({method: 'POST', url: baseUrl + 'login', data: {email: email, password: password}})
        .success(function (response) {
            return response;
        })
        .error(function (response, status) {
            return $q.reject(status);
        });
    };

    service.logout = function () {
        return $http.get(baseUrl + 'logout')
        .success(function (response) {
            return response;
        })
        .error(function (response) {
            $log.error("Error loggin out: ", response);
        });
    };

    service.getCurrentUser =  function () {
        return $http.get(baseUrl + 'currentUser').then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    return service;
}]);