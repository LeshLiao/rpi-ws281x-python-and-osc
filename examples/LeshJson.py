import json
import socket
import LeshLib

def ReadJsonFile():
    input_file = open ('rpi-ws281x-python-and-osc/examples/config/StationSetup.json')
    json_Data = json.load(input_file)
    
    print("[ StationSetup.json ]")
    print("ProjectName:" +json_Data['ProjectName'])
    print("Timestamp  :" +json_Data['Timestamp'])
    
    json_array = json_Data['MyStations']
    CurrentRuleList = []
    LeshLib.JsonTimestamp = json_Data['Timestamp']
    MatchDeviceIP = False
    
    for item in json_array:
        #print("IP:" + item['IP'])
        #print("Port:" + str(item['Port']))
        if(GetLocalIp() == item['IP']):
            CurrentRuleList = item['Rules']
            LeshLib.MyOscPort = item['Port']
            LeshLib.RuleListSize = len(CurrentRuleList)
            LeshLib.DeviceConfigList = item['Devices']
            print("We found RuleList():"+GetLocalIp()+",Rule list size:"+str(LeshLib.RuleListSize))
            MatchDeviceIP = True
            break
            
    if(MatchDeviceIP):
        InitDataWs(CurrentRuleList)
        InitDataDmx(CurrentRuleList)
        InitDataEL(CurrentRuleList)
        return True
    else:
        LeshLib.JsonTimestamp += "(No matching IP)"
        return False
    
    
DataEl = []
def InitDataEL(_ruleList): 
    global DataEl   
    DataEl.clear()  

    for index, item in enumerate(_ruleList):
        if(item['OutputType'] == "EL"):
            DataEl.append([])
            DataEl[-1].append(index)
            for _param in item['OutputParam']:
                DataEl[-1].append(_param)
            
            #print(str(index)+"item:"+item['OutputType']) 
    print("EL:")
    print(DataEl)
    
DataWsCh0 = []
DataWsCh1 = []
def InitDataWs(_ruleList): 
    global DataWsCh0   
    DataWsCh0.clear()  

    for index, item in enumerate(_ruleList):
        if(item['OutputType'] == "WS281X_Ch0"):
            LeshLib.IsWsCh00Exist = True
            DataWsCh0.append([])
            DataWsCh0[-1].append(index)
            for _param in item['OutputParam']:
                DataWsCh0[-1].append(_param)
            
            #print(str(index)+"item:"+item['OutputType']) 
    print("WS281X_Ch0:")
    print(DataWsCh0) 
    
    global DataWsCh1   
    DataWsCh1.clear()  

    for index, item in enumerate(_ruleList):
        if(item['OutputType'] == "WS281X_Ch1"):
            LeshLib.IsWsCh01Exist = True
            DataWsCh1.append([])
            DataWsCh1[-1].append(index)
            for _param in item['OutputParam']:
                DataWsCh1[-1].append(_param)
         
        
DataDmx = [] 
def InitDataDmx(_ruleList): 
    global DataDmx
    DataDmx.clear() 
    _DmxData = []

    for index, item in enumerate(_ruleList):
        if(item['OutputType'] == "DMX"):
            LeshLib.IsDmxDataExist = True
            DataDmx.append([])
            DataDmx[-1].append(index)
            _DmxData = item['OutputParam']
            for _param in item['OutputParam']:
                DataDmx[-1].append(_param)

            sum = _DmxData[0]+_DmxData[1]
            if (sum > LeshLib.DmxMaxChannel):
                LeshLib.DmxMaxChannel = sum
                
            #print(str(index)+"item:"+item['OutputType']) 
            
    LeshLib.DmxMaxChannel = LeshLib.DmxMaxChannel - 1
    print("DmxMaxChannel:"+str(LeshLib.DmxMaxChannel))
    print("DMX:") 
    print(DataDmx) 
     
def GetLocalIp(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    MyLocalIp = s.getsockname()[0]
    #print(MyLocalIp)
    s.close()
    return MyLocalIp

