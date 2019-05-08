"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
test pull latest version.2727 test....
"""
import argparse
import math
import git
import datetime

import LeshLib
import threading

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

from strandtest import *
from LeshJson import *
from pyudmx import pyudmx
from time import sleep

# global
dev = pyudmx.uDMXDevice()
#DmxBuffer = [0 for v in range(0, 32)] #TODO
DmxBuffer = []
DmxStartNum = 0
DmxDimmer = 0
TestNum = 255

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
    global DmxStartNum
    global DmxDimmer
    _dmxIndex = DmxStartNum
    _dmxDimmer = DmxDimmer
    for _data in DataDmx:
        index = _data[0]
        colorR, colorG, colorB = LeshLib.GetColorByVolume(int(_dataList[index]))
        _dmxIndex = _data[1] + _data[3] - 2  # dimmer
        DmxBuffer[_dmxIndex] = _dmxDimmer
        _dmxIndex = _data[1] + _data[4] - 2  # red
        DmxBuffer[_dmxIndex] = colorR
        _dmxIndex = _data[1] + _data[5] - 2  # green
        DmxBuffer[_dmxIndex] = colorG
        _dmxIndex = _data[1] + _data[6] - 2  # blue
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
        list1 = [GetLocalIp(),GetLocalOscPort(),sha,LeshLib.JsonTimestamp]
        client.send_message("/Response",list1)
      
    if(_commandType == "BREATHING_LIGHT"):   
        TestNum = int(_value1)
   
def job():  # gamma function?
  global TestNum
  while True:
    if(TestNum >= 0):
        if TestNum < 4: TestNum = 0
        for j in range(strip.numPixels()):
            strip.setPixelColor(j,Color(TestNum,TestNum,TestNum))
        strip.show()
        TestNum = TestNum - 4
    time.sleep(0.01)

def handler_MatrixVelocity(unused_addr, args,MarixString):

    #TODO split to 2 thread?
    tempList = MarixString.split(',')

    if (True):
        LightWS(tempList)
    if (LeshLib.IsDmxAvailible and LeshLib.IsDmxDataExist):
        LightDMX(tempList)

def WipeAllDmxLight(colorNum):
    global DataDmx  
    DmxTestList = [0 for x in range(LeshLib.RuleListSize)]
    for _data in DataDmx:
        index = _data[0]
        DmxTestList[index] = colorNum
    LightDMX(DmxTestList)

def InitDmxDevice():

    # Channel value list for channels 1-512
    cv = [0 for v in range(0, 512)]
    print("Opening DMX controller...")
    # This will automagically find a single Anyma-type USB DMX controller
    dev.open()
    # For informational purpose, display what we know about the DMX controller
    print(dev.Device)
    
    global DmxBuffer
    DmxBuffer = [0 for v in range(0, LeshLib.DmxMaxChannel)] #TODO
    #DmxBuffer = [0 for v in range(0, 512)] #TODO
    _paramData = []
    
    try:
        global DmxStartNum
        global DmxDimmer
        for index, item in enumerate(LeshLib.DeviceConfigList):
            if(item['Type'] == "DMX"):
                _paramData = item['Config']
                break
        DmxStartNum = int(_paramData[0])
        DmxDimmer = int(_paramData[1])
        
        # Turns the light all off and test dmx usb device
        cv = [0 for v in range(0, 512)]
        dev.send_multi_value(1, cv)
        LeshLib.IsDmxAvailible = True
        
        WipeAllDmxLight(3)  #W
        time.sleep(0.5)
        WipeAllDmxLight(6)  #R
        time.sleep(0.5)
        WipeAllDmxLight(21) #G
        time.sleep(0.5)
        WipeAllDmxLight(45) #B
        time.sleep(0.5)
        WipeAllDmxLight(0)  #0
        time.sleep(0.5)
        
    except:
        LeshLib.IsDmxAvailible = False
        print("DMX Warning:DMX USB Device Error...")

def InitWsDevice():
    _paramData = []
    global strip
    
    for index, item in enumerate(LeshLib.DeviceConfigList):
        if(item['Type'] == "WS281X"):
            _paramData = item['Config']
                
    booleanInvert = False
    if _paramData[4] == "1":
        booleanInvert = True
    strip = Adafruit_NeoPixel(int(_paramData[0]), int(_paramData[1]), int(_paramData[2]), int(_paramData[3]), booleanInvert, int(_paramData[5]), int(_paramData[6]),int(_paramData[7], 0))
    strip.begin()
    
    #Led Lighting Test
    colorWipe(strip, Color(255, 255, 255))  # Test Red wipe
    sleep(0.5)
    ChangeAllColorWipe(strip, Color(255, 0, 0))
    sleep(0.5)
    ChangeAllColorWipe(strip, Color(0, 255, 0))
    sleep(0.5)
    ChangeAllColorWipe(strip, Color(0, 0, 255))
    sleep(0.5)
    
    t = threading.Thread(target = job)
    t.setDaemon(True)
    t.start()

if __name__ == "__main__":
    myLocalIP = GetLocalIp()
    myLocalOscPort = GetLocalOscPort()

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",default=myLocalIP, help="The ip to listen on.")
    parser.add_argument("--port",type=int, default=myLocalOscPort, help="The port to listen on.")
    args = parser.parse_args()

    testaaa = []
    print(testaaa)
    testaaa = [0 for v in range(0, 5)] 
    print(testaaa)

    # Initial
    LeshLib.init_global_var()
    ReadJsonFile()
    InitWsDevice()
    InitDmxDevice()
    
    # OSC Server
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/MatrixVelocity", handler_MatrixVelocity,"PrintValue")
    dispatcher.map("/Instruction", handler_Instruction,"test1","test2")
    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("OSC Serving on {}".format(server.server_address))
    server.serve_forever()

