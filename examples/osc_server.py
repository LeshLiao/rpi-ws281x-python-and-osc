"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
test pull latest version.333
"""
import argparse
import math

import LeshLib
import threading

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

from strandtest import *
from LeshJson import *


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
    global DataWs  

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
        client = udp_client.SimpleUDPClient(_value1, int(_value2))
        list1 = [GetLocalIp(),GetLocalOscPort()]
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
        
    if (True):
        LightDMX(tempList)

    """
    tempList = MarixString.split(',')
    ListIndex = 0
    maxlen = len(tempList)-1
    for i in range(0,maxlen):
        tempInt = int(tempList[i])
        colorR, colorG, colorB = LeshLib.GetColorByVolume(tempInt)
        strip.setPixelColor(i,Color(colorR,colorG,colorB))
    strip.show()
    #$print("print_handler_TagAndVelocity:[{0}]:{1},{2}".format(args[0],args[1],args[2]))
    """


def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

if __name__ == "__main__":
  myLocalIP = GetLocalIp()
  myLocalOscPort = GetLocalOscPort()
  
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default=myLocalIP, help="The ip to listen on.")
  parser.add_argument("--port",
      type=int, default=myLocalOscPort, help="The port to listen on.")
  args = parser.parse_args()

  #10.1.1.6
  
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
  
  ReadJsonFile()
  
  server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
  print("Serving on(test01) {}".format(server.server_address))
  server.serve_forever()
  
  
