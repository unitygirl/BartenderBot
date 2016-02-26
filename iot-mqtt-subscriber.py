#!/usr/bin/python3
 
#required libraries
import sys
import ssl
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

#called while client tries to establish connection with the server
def on_connect(mqttc, obj, flags, rc):
    print("in onConnect")
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")
    #the topic to publish to
    mqttc.subscribe("$aws/things/AlexaPi/shadow/update/#", 0) #The names of these topics start with $aws/things/thingName/shadow."
    print("called subscribe()")
#called when a topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))
   

#called when a message is received by a topic
def on_message(mqttc, obj, msg):
    print("Received message from topic: "+msg.topic+" | QoS: "+str(msg.qos)+" | Data Received: "+str(msg.payload))
    if str(msg.payload) == "b'negroni'":
        MotorPin1   = 18    
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)          # Numbers GPIOs by physical location
        GPIO.setup(MotorPin1, GPIO.OUT)   # mode --- output
        GPIO.output(MotorPin1, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(MotorPin1, GPIO.LOW)
    else:
        print("Drink not found")

#creating a client with client-id=mqtt-test
mqttc = mqtt.Client()
motor = "ON"

print("called Client()")

mqttc.on_connect = on_connect
print("called onConnect()")
mqttc.on_subscribe = on_subscribe
print("called onSubscribe()")
mqttc.on_message = on_message
print("called onMessage()")

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set("/home/pi/awsiot/root-CA.crt",
              certfile="/home/pi/awsiot/32935e74fe-certificate.pem.crt",
              keyfile="/home/pi/awsiot/32935e74fe-private.pem.key",
              tls_version=ssl.PROTOCOL_TLSv1_2,
              ciphers=None)
print("called tls_set()")
#connecting to aws-account-specific-iot-endpoint
mqttc.connect("ALOFHZJZ1DP7D.iot.us-west-2.amazonaws.com", 8883, 60) #AWS IoT service hostname and portno
print("called connect()")




#automatically handles reconnecting
mqttc.loop_forever()
