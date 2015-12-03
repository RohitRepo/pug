angular.module("module.model")
.factory("deviceModel", ['$http', '$q', function ($http, $q) {
    var service = {};

    var baseUrl = '/api/v1/devices/'

    service.device_on = function (device_id) {
        return $http({method: 'POST', url: baseUrl + device_id + '/turn_on'})
        .success(function (response) {
            return response;
        })
        .error(function (response, status) {
            return $q.reject(status);
        });
    };

    service.device_off = function (device_id) {
        return $http({method: 'POST', url: baseUrl + device_id + '/turn_off'})
        .success(function (response) {
            return response;
        })
        .error(function (response, status) {
            return $q.reject(status);
        });
    };

    service.myDevices =  function () {
        return $http.get(baseUrl + 'my').then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    return service;
}]);