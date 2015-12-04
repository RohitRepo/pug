import json
import paho.mqtt.client as mqtt

from django.conf import settings

from devices.models import Device


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    if not rc:
	    mqttc.subscribe(settings.UPDATE_TOPICS, 1)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def process_updates(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        device = Device.objects.get(pk=data['id'])
        if data['status'] == 'on':
            device.status = True
        elif data['status'] == 'off':
            device.status = False

        device.connected = True
        device.save()


    except Device.DoesNotExist:
        print "Could not find the corresponding device"
    except Exception as e:
        print "Error processing update"
        print e.message

def process_last_wills(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        device = Device.objects.get(pk=data['id'])

        device.connected = False;
        device.save()

    except Device.DoesNotExist:
        print "Could not find the corresponding device"
    except Exception as e:
        print "Error processing update"
        print e.message

mqttc = mqtt.Client(client_id="2345", clean_session=False)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.message_callback_add(settings.UPDATE_TOPICS, process_updates)
mqttc.message_callback_add(settings.LAST_WILL_TOPICS, process_last_wills)

mqttc.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
mqttc.connect(settings.MQTT_SERVER, settings.MQTT_PORT, 60)
mqttc.loop_start()