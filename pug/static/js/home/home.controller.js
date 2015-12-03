angular.module("HomeApp")
.controller("homeController", ['$scope', 'userModel', function ($scope, userModel) {

    $scope.loginFailed = false;
    $scope.user = {};

    $scope.login = function () {
        $scope.loginFailed = false;

        userModel.login($scope.user.email, $scope.user.password).then(function () {
            window.location = '/home';
        }, function () {
            $scope.loginFailed = true;
        })
    };
}]);