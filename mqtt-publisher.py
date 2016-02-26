#!/usr/bin/python3

#required libraries
import sys
import ssl
import paho.mqtt.client as mqtt

#called while client tries to establish connection with the server
def on_Connect(mqttc, obj, flags, rc):
    print("in onConnect")
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")
    #publish message
    mqttc.publish("$aws/things/AlexaPi/shadow/update/", payload="negroni", qos=0, retain=False)
    print ("message published")


def iot_connect():
#creating a client with client-id=mqtt-test
mqttc = mqtt.Client()
print("called Client()")
mqttc.on_connect = on_Connect
print("called onConnect()")


#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set("/home/pi/awsiot/root-CA.crt",
              certfile="/home/pi/awsiot/32935e74fe-certificate.pem.crt",
              keyfile="/home/pi/awsiot/32935e74fe-private.pem.key",
              tls_version=ssl.PROTOCOL_TLSv1_2,
              ciphers=None)
print("called tls_set()")
#connecting to aws-account-specific-iot-endpoint
mqttc.connect("ALOFHZJZ1DP7D.iot.us-west-2.amazonaws.com", port=8883) #AWS IoT service hostname and portno
print("called connect()")

#automatically handles reconnecting
mqttc.loop_forever()
