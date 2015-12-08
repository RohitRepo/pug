import json
import paho.mqtt.client as mqtt

from django.conf import settings

from devices.models import Device


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    if not rc:
	    mqttc.subscribe([(settings.UPDATE_TOPICS, 1), (settings.CONNECT_TOPICS, 1), (settings.LAST_WILL_TOPICS, 1)])

def on_disconnect(client, userdata, rc):
	print("Disconnect with result code "+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_log(mosq, obj, level, string):
    print(string)

def process_connects(client, userdata, msg):
    print("Got connect " + msg.topic+" "+str(msg.payload))

    try:
    	device_id = msg.topic[17:]
        device = Device.objects.get(pk=device_id)

        device.connected = True
        device.ip = msg.payload;
        device.save()


    except Device.DoesNotExist:
        print "Could not find the corresponding device"
    except Exception as e:
        print "Error processing connect"
        print e.message

def process_updates(client, userdata, msg):
    print("Got update " + msg.topic+" "+str(msg.payload))
    try:
    	device_id = msg.topic[16:]
        device = Device.objects.get(pk=device_id)
        if msg.payload == 'on':
            device.status = True
        elif msg.payload == 'off':
            device.status = False

        device.connected = True
        device.save()


    except Device.DoesNotExist:
        print "Could not find the corresponding device"
    except Exception as e:
        print "Error processing update"
        print e.message

def process_last_wills(client, userdata, msg):
    print("Got last will" + msg.topic+" "+str(msg.payload))
    try:
        device_id = msg.topic[13:]
        device = Device.objects.get(pk=device_id)

        device.connected = False;
        device.save()

    except Device.DoesNotExist:
        print "Could not find the corresponding device"
    except Exception as e:
        print "Error processing last"
        print e.message

mqttc = mqtt.Client(client_id="2345", clean_session=False)
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message
mqttc.on_log = on_log
mqttc.message_callback_add(settings.UPDATE_TOPICS, process_updates)
mqttc.message_callback_add(settings.CONNECT_TOPICS, process_connects)
mqttc.message_callback_add(settings.LAST_WILL_TOPICS, process_last_wills)

mqttc.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
mqttc.loop_start()
mqttc.connect(settings.MQTT_SERVER, settings.MQTT_PORT, 60)