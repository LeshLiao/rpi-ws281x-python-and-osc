"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
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

def handler_Instruction(unused_addr, args,_value):
    
    print("Instruction Start")
    print("Value="+str(_value))
    print("Instruction End")
    
    global TestNum
    TestNum = 255
    
    client = udp_client.SimpleUDPClient("172.20.10.4", 2349)
    client.send_message("/Response",112233)
   
def job():
  #for i in range(5):
  global TestNum
  while True:
    if(TestNum > 0):
        for j in range(8):
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
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default=myLocalIP, help="The ip to listen on.")
  parser.add_argument("--port",
      type=int, default=2346, help="The port to listen on.")
  args = parser.parse_args()

  #10.1.1.6
  
  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/MatrixVelocity", handler_MatrixVelocity,"PrintValueAAA")
  dispatcher.map("/Instruction", handler_Instruction,"test")
  
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
  
  
