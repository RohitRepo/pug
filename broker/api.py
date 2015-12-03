import json
from paho.mqtt.client import MQTT_ERR_SUCCESS

from .client import mqttc

from devices.models import Device

def turn_device_on(device_id):
	topic = "devices/actions/" + str(device_id)
	payload = "on"
	result, mid = mqttc.publish(topic, payload = payload, qos=1)
    if result == MQTT_ERR_SUCCESS:
        return True
    return False

def turn_device_off(device_id):
	topic = "devices/actions/" + str(device_id)
	payload = "off"
    result, mid = mqttc.publish(topic, payload = payload, qos=1)
    if result == MQTT_ERR_SUCCESS:
        return True
    return False

def start_client():
	mqttc.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
	mqttc.connect(settings.MQTT_SERVER, settings.MQTT_PORT, 60)
	mqttc.loop_start()

def stop_client():
	mqttc.loop_stop()