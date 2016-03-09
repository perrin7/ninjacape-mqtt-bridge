#!/usr/bin/python
#
# used to interface the NinjaCape to openHAB via MQTT
# - reads data from serial port and publishes on MQTT client
# - writes data to serial port from MQTT subscriptions
#
# - uses the Python MQTT client from the Mosquitto project http://mosquitto.org (now in Paho)
#
# https://github.com/perrin7/ninjacape-mqtt-bridge
# perrin7
 
import serial
import paho.mqtt.client as mqtt
import os
import json
import threading
import time

### Settings
serialdev = '/dev/ttyO1'
broker = "server.local" # mqtt broker
port = 1883 # mqtt broker port

debug = False  ## set this to True for lots of prints

# buffer of data to output to the serial port
outputData = []
 
####  MQTT callbacks
def on_connect(client, userdata, flags, rc):
	if rc == 0:
	#rc 0 successful connect
		print "Connected"
	else:
		raise Exception
	#subscribe to the output MQTT messages
	output_mid = client.subscribe("ninjaCape/output/#")
 
def on_publish(client, userdata, mid):
	if(debug):
		print "Published. mid:", mid

def on_subscribe(client, userdata, mid, granted_qos):
	if(debug):
		print "Subscribed. mid:", mid

def on_message_output(client, userdata, msg):
	if(debug):
		print "Output Data: ", msg.topic, "data:", msg.payload
	#add to outputData list
	outputData.append(msg)

def on_message(client, userdata, message):
	if(debug):
		print "Unhandled Message Received: ", message.topic, message.paylod		

#called on exit
#close serial, disconnect MQTT
def cleanup():
	print "Ending and cleaning up"
	ser.close()
	mqttc.disconnect()

def mqtt_to_JSON_output(mqtt_message):
	topics = mqtt_message.topic.split('/');
	## JSON message in ninjaCape form
	json_data = '{"DEVICE": [{"G":"0","V":0,"D":' + topics[2] + ',"DA":"' + mqtt_message.payload + '"}]})'
	return json_data

#thread for reading serial data and publishing to MQTT client
def serial_read_and_publish(ser, mqttc):
	ser.flushInput()
	
	lastMessage = ""
	lastMessageTime = time.time()

	while True:
		line = ser.readline() # this is blocking
		if(debug):
			print "line to decode:",line
		
		# split the JSON packet up here and publish on MQTT
		json_data = json.loads(line)
		if(debug):
			print "json decoded:",json_data

		try:
			theTime = time.time()
			device = str( json_data['DEVICE'][0]['D'] )
			data = str( json_data['DEVICE'][0]['DA'] )
		
		# code to 'debounce' the inputs - maximum of one message per 2 seconds from each device	
			if(lastMessageTime + 2.0 < theTime):
				if(debug):
					print "enough time between lmt: " + str(lastMessageTime) + " theTime: " + str(theTime)
				mqttc.publish("ninjaCape/input/"+device, data)
				lastMessage = device+data
				lastMessageTime = theTime
			elif(lastMessage != device+data):
				if(debug):
					print "different messages lm:" + lastMessage + " cm:" + device+data
				mqttc.publish("ninjaCape/input/"+device, data)
				lastMessage = device+data
				lastMessageTime = theTime
			else:
				if(debug):
					print "debounce!!!!!!"
				# do nothing!

		except(KeyError):
			# TODO should probably do something here if the data is malformed
			pass

############ MAIN PROGRAM START
try:
	print "Connecting... ", serialdev
	#connect to serial port
	ser = serial.Serial(serialdev, 9600, timeout=None) #timeout 0 for non-blocking. Set to None for blocking.

except:
	print "Failed to connect serial"
	#unable to continue with no serial input
	raise SystemExit

try:
	#create an mqtt client
	mqttc = mqtt.Client("ninjaCape")

	#attach MQTT callbacks
	mqttc.on_connect = on_connect
	mqttc.on_publish = on_publish
	mqttc.on_subscribe = on_subscribe
	mqttc.on_message = on_message
	mqttc.message_callback_add("ninjaCape/output/#", on_message_output)

	#connect to broker
	mqttc.connect(broker, port, 60)

	# start the mqttc client thread
	mqttc.loop_start()
	
	serial_thread = threading.Thread(target=serial_read_and_publish, args=(ser, mqttc))
	serial_thread.daemon = True
	serial_thread.start()
		
	while True: # main thread
		#writing to serial port if there is data available
		if( len(outputData) > 0 ):
			#print "***data to OUTPUT:",mqtt_to_JSON_output(outputData[0])
			ser.write(mqtt_to_JSON_output(outputData.pop()))

		time.sleep(0.5)

# handle app closure
except (KeyboardInterrupt):
	print "Interrupt received"
	cleanup()
except (RuntimeError):
	print "uh-oh! time to die"
	cleanup()
