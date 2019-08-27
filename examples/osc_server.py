"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
test pull latest version.4040 test....
"""
import argparse
import math
import git
import datetime
import pyfirmata

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
DmxBuffer = []
DmxStartNum = 0
DmxDimmer = 0
TestNum = 255

def LightEL(_RgbList):
    global DataEl  
    for _data in DataEl:
        index = _data[0]
        pin_num = _data[1]
        baseIndex = index * 3
        colorR =  int(_RgbList[baseIndex])
        colorG =  int(_RgbList[baseIndex+1])
        colorB =  int(_RgbList[baseIndex+2])
        if((colorR > 0) or (colorG > 0) or (colorB > 0) ):
            LeshLib.ElDevice[pin_num].write(1)
        else:
            LeshLib.ElDevice[pin_num].write(0)


def LightWS(_RgbList):
    global DataWs  
    for _data in DataWs:
        index = _data[0]
        #colorR, colorG, colorB = LeshLib.GetColorByVolume(int(_velocityList[index]))
        baseIndex = index * 3
        colorR = int(_RgbList[baseIndex])
        colorG =  int(_RgbList[baseIndex+1])
        colorB =  int(_RgbList[baseIndex+2])
        
        for j in range(_data[1],_data[2]):
            #print(str(j)+',')
            strip.setPixelColor(j,Color(colorR,colorG,colorB))
        #print('|')
    strip.show()

def LightDMX(_RgbList):
    global DataDmx  
    global DmxBuffer
    global DmxStartNum
    global DmxDimmer
    _dmxIndex = DmxStartNum
    _dmxDimmer = DmxDimmer
    for _data in DataDmx:
        index = _data[0]
        #colorR, colorG, colorB = LeshLib.GetColorByVolume(int(_velocityList[index]))
        baseIndex = index * 3
        colorR =  int(_RgbList[baseIndex])
        colorG =  int(_RgbList[baseIndex+1])
        colorB =  int(_RgbList[baseIndex+2])
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
    print("_unusedAddr="+_unusedAddr)
    
    #for _arg in args:
    #    print("_arg="+_arg)
        
    print("_commandType="+_commandType)
    print("_value1="+_value1)
    print("_value2="+_value2)

    if(_commandType == "RELOAD_JSON"):
        if(ReadJsonFile()):
            InitWsDevice()
            InitDmxDevice()
            InitElDevice()
        else:
            print("No match device setting in Json file:"+GetLocalIp())
        ReportDeviceInfo(Master_args.ip,Master_args.port)
        print("RELOAD_JSON")
        
    if(_commandType == "CHECK_OSC"):
        ReportDeviceInfo(_value1,_value2)
      
    if(_commandType == "BREATHING_LIGHT"):   
        TestNum = int(_value1)

def ReportDeviceInfo(_ip,_port):
    client = udp_client.SimpleUDPClient(_ip, int(_port))
    path = "/home/pi/rpi-ws281x-python-and-osc"
    repo = git.Repo(path, search_parent_directories=True)
    sha = repo.head.object.hexsha
    temp_list = [GetLocalIp(),LeshLib.MyOscPort,sha,LeshLib.JsonTimestamp]
    client.send_message("/Response",temp_list)

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

def handler_MatrixVelocity(unused_addr, args,VelocityString):
    #TODO split to 2 thread?
    _velocityList = VelocityString.split(',')
    if (True):
        LightWS(_velocityList)
    if (LeshLib.IsDmxAvailible and LeshLib.IsDmxDataExist):
        LightDMX(_velocityList)
    if (LeshLib.IsElAvailible):
        LightEL(_velocityList)

def WipeAllDmxLight(colorR,colorG,colorB):
    global DataDmx  
    DmxTestRgbList = [0 for x in range(LeshLib.RuleListSize*3)]
    for _data in DataDmx:
        index = _data[0]
        baseIndex = index *3
        DmxTestRgbList[baseIndex] = colorR
        DmxTestRgbList[baseIndex+1] = colorG
        DmxTestRgbList[baseIndex+2] = colorB
    LightDMX(DmxTestRgbList)

def InitElDevice():
    _paramData = []
    ConfigDataExist = False
    for index, item in enumerate(LeshLib.DeviceConfigList):
        if(item['Type'] == "EL"):
            _paramData = item['Config']
            ConfigDataExist = True
            break

    if(ConfigDataExist):
        print("Initail EL Device...")
        print("loading "+_paramData[0])
        
        try:
            board = pyfirmata.Arduino(_paramData[0])
            LeshLib.IsElAvailible = True
            LeshLib.ElDevice = [None]*(int(_paramData[2])+1)
            for pin_num in range(int(_paramData[1]),int(_paramData[2])):
                pin_status = "d:"+ str(pin_num) + ":o"
                print("    GPIO:"+pin_status)
                LeshLib.ElDevice[pin_num] = board.get_pin(pin_status)
        except:
            LeshLib.IsElAvailible = False
            print("[Warning]:EL Wire USB Device Error...")


def InitDmxDevice():
    print("Opening DMX(0)")
    _paramData = []
    ConfigDataExist = False
    for index, item in enumerate(LeshLib.DeviceConfigList):
        if(item['Type'] == "DMX"):
            _paramData = item['Config']
            ConfigDataExist = True
            break
    print("Opening DMX(1)")
    if(ConfigDataExist):
        print("Initail DMX Device...")
        # Channel value list for channels 1-512
        cv = [0 for v in range(0, 512)]
        print("Opening DMX(2)")
        #print("Opening DMX controller...")
        # This will automagically find a single Anyma-type USB DMX controller
        dev.open()
        # For informational purpose, display what we know about the DMX controller
        #print(dev.Device)
        print("Opening DMX(3)")
        global DmxBuffer
        DmxBuffer = [0 for v in range(0, LeshLib.DmxMaxChannel)]
        
        try:
            global DmxStartNum
            global DmxDimmer

            DmxStartNum = int(_paramData[0])
            DmxDimmer = int(_paramData[1])
            
            # Turns the light all off and test dmx usb device
            cv = [0 for v in range(0, 512)]
            dev.send_multi_value(1, cv)
            LeshLib.IsDmxAvailible = True
            print("Opening DMX(4)")
            WipeAllDmxLight(255,255,255)  #W
            time.sleep(0.5)
            WipeAllDmxLight(255,0,0)  #R
            time.sleep(0.5)
            WipeAllDmxLight(0,255,0) #G
            time.sleep(0.5)
            WipeAllDmxLight(0,0,255) #B
            time.sleep(0.5)
            WipeAllDmxLight(0,0,0)  #0
            time.sleep(0.5)
            print("Opening DMX(5)")
            
        except:
            LeshLib.IsDmxAvailible = False
            print("[Warning]:DMX USB Device Error...")

def InitWsDevice():
    _paramData = []
    ConfigDataExist = False
    for index, item in enumerate(LeshLib.DeviceConfigList):
        if(item['Type'] == "WS281X"):
            _paramData = item['Config']
            ConfigDataExist = True
            break
    
    if(ConfigDataExist):
        print("Initail WS Device...")
        booleanInvert = False
        if _paramData[4] == "1":
            booleanInvert = True
            
        global strip
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",default="127.0.0.1", help="Master IP")
    parser.add_argument("--port",type=int, default=2349, help="Master port")
    Master_args = parser.parse_args()

    # Initial
    LeshLib.init_global_var()
    if(ReadJsonFile()):
        InitWsDevice()
        InitDmxDevice()
        InitElDevice()
    else:
        print("No match device setting in Json file:"+GetLocalIp())
    
    # OSC Server
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/MatrixVelocity", handler_MatrixVelocity,"PrintValue")
    dispatcher.map("/Instruction", handler_Instruction,"test1","test2")
    server = osc_server.ThreadingOSCUDPServer((GetLocalIp(),LeshLib.MyOscPort), dispatcher)
    print("OSC Serving on {}".format(server.server_address))
    
    # Reply status to master
    ReportDeviceInfo(Master_args.ip,Master_args.port)
    server.serve_forever()
    
    

