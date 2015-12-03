angular.module("ProfileApp")
.controller("profileController", ['$scope', 'deviceModel', function ($scope, deviceModel) {

    $scope.getttingDevices = true;
    deviceModel.myDevices().then(function (devices) {
        $scope.getttingDevices = false;
        $scope.devices = devices;

        if ($scope.devices.length == 0){
            $scope.noDevices = true;
        }
    }, function () {
        $scope.getttingDevices = false;
    });
}]);