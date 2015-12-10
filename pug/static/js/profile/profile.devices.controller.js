angular.module("ProfileApp")
.controller("profileDevicesController", ['$scope', 'deviceModel', function ($scope, deviceModel) {

    function onConnectionLost (response) {
        if (response.errorCode !== 0) {
            console.log("onConnectionLost:" + response.errorMessage);
        }
    };

    function handle_update (topic, response) {
        console.log("handle update", {topic: topic, response: response})
        var id = topic.substring(16,topic.length);
        console.log("got id:", id);

        for (i=0; i< $scope.devices.length; i++){

            if ($scope.devices[i].device_id == id) {

                $scope.$apply(function () {
                    if (response == "on") {
                        $scope.devices[i].status = true;
                        $scope.devices[i].connected = true;
                    } else if (response == "off") {
                        $scope.devices[i].status = false;
                        $scope.devices[i].connected = true;
                    }
                });
                break;
            }
        }
    };

    function handle_connect (topic, response) {
        var id = topic.substring(17,topic.length);
        for (i=0; i< $scope.devices.length; i++){

            if ($scope.devices[i].device_id == id) {

                $scope.$apply(function () {
                    $scope.devices[i].connected = true;
                });
                break;
            }
        }
    };

    function handle_last_will (topic, response) {
        console.log("handle last");
        var id = topic.substring(13,topic.length);

        for (i=0; i< $scope.devices.length; i++){

            if ($scope.devices[i].device_id == id) {

                $scope.$apply(function () {
                    $scope.devices[i].connected = false;
                });
                break;
            }
        }
    };

    function onMessageArrived (message) {
        var messageObj = {
            'topic': message.destinationName,
            'retained': message.retained,
            'qos': message.qos,
            'payload': message.payloadString,
        };

        console.log("got message", messageObj);

        // var response = jQuery.parseJSON();
        var topic = message.destinationName;

        if (topic.startsWith("devices/updates")) {
            handle_update(topic, message.payloadString);
        } else if (topic.startsWith("devices/last")) {
            handle_last_will(topic, message.payloadString);
        } else if (topic.startsWith("devices/connects")) {
            handle_connect(topic, message.payloadString);
        }
    };

    var client = new Paho.MQTT.Client('m11.cloudmqtt.com', 32911, clientId='');
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    function onConnect () {
        console.log("Client connected");

        for (i=0; i< $scope.devices.length; i++){
            client.subscribe("devices/updates/" + $scope.devices[i].device_id, {qos: 1})
            client.subscribe("devices/last/" + $scope.devices[i].device_id, {qos: 1})
            client.subscribe("devices/connects/" + $scope.devices[i].device_id, {qos: 1})
        }
    };

    function onFail (message) {
        console.log("Connection failed ", message);
    };

    function connect_client () {
        var options = {
            useSSL: true,
            onSuccess: onConnect,
            onFailure: onFail,
            userName: 'client',
            password: 'thelazybum'
        }
        client.connect(options);
    };

    $scope.getttingDevices = true;

    deviceModel.myDevices().then(function (devices) {
        $scope.getttingDevices = false;
        $scope.devices = devices;

        if ($scope.devices.length == 0){
            $scope.noDevices = true;
        }
        connect_client();
    }, function () {
        $scope.getttingDevices = false;
    });

    $scope.getBackground = function (device) {
        if (!device.connected) {
            return '#333333';
        }

        if (device.status) {
            return '#336600';
        } else {
            return '#993300';
        }
    };

    $scope.getDeviceStatus = function (device) {
        if (!device.connected) {
            return 'OFFLINE';
        }

        if (device.status) {
            return 'ON';
        } else {
            return 'OFF';
        }
    };

    $scope.toggleDevice = function (device) {
        if (!device.connected) {
            return;
        }

        device.toggling = true;

        if (device.status) {
            deviceModel.device_off(device.id).then(function () {
                device.toggling = false;
            }, function () {
                device.toggling = false;
            });
        } else {
            deviceModel.device_on(device.id).then(function () {
                device.toggling = false;
            }, function () {
                device.toggling = false;
            });
        }
    };
}]);