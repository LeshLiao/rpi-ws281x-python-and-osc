"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
test pull latest version.2727 test....
"""
import argparse
import math
import git

import LeshLib
import threading

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

from strandtest import *
from LeshJson import *
from pyudmx import pyudmx
from time import sleep


dev = pyudmx.uDMXDevice()
DmxBuffer = [0 for v in range(0, 256)]

def LightWS(_dataList):
    global DataWs  
    for _data in DataWs:
        index = _data[0]
        colorR, colorG, colorB = LeshLib.GetColorByVolume(int(_dataList[index]))
        for j in range(_data[1],_data[2]):
            #print(str(j)+',')
            strip.setPixelColor(j,Color(colorR,colorG,colorB))
        #print('|')
    strip.show()

def LightDMX(_dataList):
    global DataDmx  
    global DmxBuffer
    _dmxIndex = 0
    _dmxDimmer = 64
    for _data in DataDmx:
        index = _data[0]
        colorR, colorG, colorB = LeshLib.GetColorByVolume(int(_dataList[index]))
        _dmxIndex = _data[1] + _data[3] - 1  # dimmer
        DmxBuffer[_dmxIndex] = _dmxDimmer
        _dmxIndex = _data[1] + _data[4] - 1  # red
        DmxBuffer[_dmxIndex] = colorR
        _dmxIndex = _data[1] + _data[5] - 1  # green
        DmxBuffer[_dmxIndex] = colorG
        _dmxIndex = _data[1] + _data[6] - 1  # blue
        DmxBuffer[_dmxIndex] = colorB
        
    sent = dev.send_multi_value(1, DmxBuffer)
    return sent    

def handler_Instruction(_unusedAddr, args,_commandType,_value1,_value2):
    global TestNum
    print("aaa")
    print("_unusedAddr="+_unusedAddr)
    
    #for _arg in args:
    #    print("_arg="+_arg)
        
    print("_commandType="+_commandType)
    print("_value1="+_value1)
    print("_value2="+_value2)

    if(_commandType == "RELOAD_JSON"):
        ReadJsonFile()
        print("RELOAD_JSON")
        
    if(_commandType == "CHECK_OSC"):
        path = "/home/pi/rpi-ws281x-python-and-osc"
        repo = git.Repo(path, search_parent_directories=True)
        sha = repo.head.object.hexsha

        client = udp_client.SimpleUDPClient(_value1, int(_value2))
        list1 = [GetLocalIp(),GetLocalOscPort(),sha]
        client.send_message("/Response",list1)
      
    if(_commandType == "BREATHING_LIGHT"):   
        TestNum = int(_value1)
   
def job():
  #for i in range(5):
  global TestNum
  while True:
    if(TestNum >= 0):
        for j in range(strip.numPixels()):
            strip.setPixelColor(j,Color(TestNum,TestNum,TestNum))
        #print("Child thread:", TestNum)
        strip.show()
        TestNum = TestNum - 4
    time.sleep(0.01)

def handler_MatrixVelocity(unused_addr, args,MarixString):

    tempList = MarixString.split(',')
    if (True):
        LightWS(tempList)
    if (LeshLib.IsDmxAvailible and LeshLib.IsDmxDataExist):
        LightDMX(tempList)

 
  
def send_rgb(dev,channel, red, green, blue, dimmer):
    """
    Send a set of RGB values to the light
    """
   
    
    #cv = [0 for v in range(0, 512)]
    cv = [0 for v in range(0, 256)]
    cv[0] = dimmer
    cv[1] = red
    cv[2] = green
    cv[3] = blue
    sent = dev.send_multi_value(channel, cv)
    return sent


def main_dmx_test():

    """
    How to control a DMX light through an Anyma USB controller
    """
    # Channel value list for channels 1-512
    cv = [0 for v in range(0, 512)]
    # Create an instance of the DMX controller and open it    
    print("Opening DMX controller...")
    
    # This will automagically find a single Anyma-type USB DMX controller
    dev.open()
    # For informational purpose, display what we know about the DMX controller
    print(dev.Device)
    
    # Here's an easier way to do it

    print("And, again the easier way")
    
    try:
        send_rgb(dev,1, 255, 0, 0, 128)
        sleep(0.5)
        send_rgb(dev,1, 0, 255, 0, 128)
        sleep(0.5)
        send_rgb(dev,1, 0, 0, 255, 128)
        sleep(0.5)
        
        send_rgb(dev,9, 255, 0, 0, 128)
        sleep(0.5)
        send_rgb(dev,9, 0, 255, 0, 128)
        sleep(0.5)
        send_rgb(dev,9, 0, 0, 255, 128)
        sleep(0.5)
       
        print("Reset all channels and close..")
        # Turns the light off
        cv = [0 for v in range(0, 512)]
        
        dev.send_multi_value(1, cv)
        LeshLib.IsDmxAvailible = True
    except:
        LeshLib.IsDmxAvailible = False
        print("DMX Warning:DMX USB Device Error...")
    #dev.close()

    
if __name__ == "__main__":
  myLocalIP = GetLocalIp()
  myLocalOscPort = GetLocalOscPort()
  
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default=myLocalIP, help="The ip to listen on.")
  parser.add_argument("--port",
      type=int, default=myLocalOscPort, help="The port to listen on.")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/MatrixVelocity", handler_MatrixVelocity,"PrintValueAAA")
  dispatcher.map("/Instruction", handler_Instruction,"test1","test2")
  
  #initled()
  #opt_parse()
  
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  strip.begin()
  colorWipe(strip, Color(255, 255, 255))  # White wipe
  
  TestNum = 255
  t = threading.Thread(target = job)
  t.setDaemon(True)
  t.start()
  
  LeshLib.init_global_var()
  ReadJsonFile()
  main_dmx_test()
  
  server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
  
  
