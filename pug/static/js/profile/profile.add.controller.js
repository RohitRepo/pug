angular.module("ProfileApp")
.controller("profileAddController", [
    '$scope',
    '$state',
    'deviceModel',
    function ($scope, $state, deviceModel) {

    $scope.device = {};

    $scope.addDevice = function () {
        $scope.validationFailed = true;

        deviceModel.validate($scope.device.device_id, $scope.device.code).then(function () {
            $state.go('devices');
        }, function (response) {
            $scope.validationFailed = true;

            var status = response.status;

            if (status == '404') {
                $scope.validationError = 'No such device could be found. Please check the device id';
            } else if ( status == '406') {
                $scope.validationError = 'Invalid validation code';
            } else {
                $scope.validationError = 'Unable to add device';
            }
        });
    };

}]);