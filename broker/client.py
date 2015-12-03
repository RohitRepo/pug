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
    print("Got update " + msg.topic+" "+str(msg.payload))

    try:
    	data = json.loads(msg.payload)
    	print "got data"
    	print data
    	device = Device.objects.get(pk=data['id'])
    	if data['status'] == 'on':
    		device.status = True
    	elif data['status'] == 'off':
    		device.satus = False

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