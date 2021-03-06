#!/usr/bin/env python
# Title : intercom_demo.py
# Author : Kyna Mowat-Gosnell
# Date : 09/10/17
# Version : 2.0

import rospy, qi, argparse
import sys
import time
import naoqi
from naoqi import *
from diagnostic_msgs.msg import KeyValue # message type /iot_updates uses
from std_msgs.msg import Empty

def callback(data):
	print("inside callback")

def iot_callback(data):
    if(data.key == "Hall_Intcm" and data.value == "ON"): # Button pressed
        intcm_ring()

def intcm_ring():
    ttsProxy.say("The intercom feed can be streamed on robots")
    #animatedProxy.say("There is someone at the door")
    tabletProxy.showWebview("http://192.168.1.121/apps/webview-6b6450/index.html")
    #tabletProxy.showWebview("http://192.168.1.99/mjpg/video.mjpg")
    #tabletProxy.showWebview("http://192.168.1.99/jpg/image.jpg")
    time.sleep(10)
    tabletProxy.hideWebview()

def listener():
    rospy.init_node('intcm_listener', anonymous=True) # initialise node to subscribe to topic
    rospy.Subscriber("/devices/bell", Empty, callback) # subscribe to topic /iot_updates
    rospy.Subscriber("/iot_command", KeyValue, iot_callback)
    rospy.spin() # keeps python from exiting until node is stopped


if __name__ == '__main__':
    from naoqi import ALProxy
    # Create a local broker, connected to the remote naoqi
    broker = ALBroker("pythonBroker", "192.168.1.129", 9999, "pepper.local", 9559)
    #animatedProxy = ALProxy("ALAnimatedSpeech", "pepper.local", 9559) # initialise animated speech proxy
    ttsProxy = ALProxy("ALTextToSpeech", "pepper.local", 9559)
    tabletProxy = ALProxy("ALTabletService", "pepper.local", 9559)
    tabletProxy.getWifiStatus() # check wifi status
    print tabletProxy.getWifiStatus() # print wifi status "CONNECTED" if connected
    postureProxy = ALProxy("ALRobotPosture", "pepper.local", 9559) # initialise posture proxy
    postureProxy.goToPosture("StandInit", 0.5) # return to initial position

    while True:
        listener()
