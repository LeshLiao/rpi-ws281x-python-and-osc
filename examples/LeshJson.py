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
    
    for item in json_array:
        #print("IP:" + item['IP'])
        #print("Port:" + str(item['Port']))
        if(GetLocalIp() == item['IP']):
            CurrentRuleList = item['Rules']
            LeshLib.RuleListSize = len(CurrentRuleList)
            LeshLib.DeviceConfigList = item['Devices']
            print("We found RuleList():"+GetLocalIp()+",Rule list size:"+str(LeshLib.RuleListSize))
            break
    InitDataWs(CurrentRuleList)
    InitDataDmx(CurrentRuleList)

    
DataWs = []
def InitDataWs(_ruleList): 
    global DataWs   
    DataWs.clear()  

    for index, item in enumerate(_ruleList):
        if(item['OutputType'] == "WS281X"):
            DataWs.append([])
            DataWs[-1].append(index)
            for _param in item['OutputParam']:
                DataWs[-1].append(_param)
            
            #print(str(index)+"item:"+item['OutputType']) 
    print("WS281X:")
    print(DataWs) 
         
        
DataDmx = [] 
def InitDataDmx(_ruleList): 
    global DataDmx
    DataDmx.clear() 

    for index, item in enumerate(_ruleList):
        if(item['OutputType'] == "DMX"):
            LeshLib.IsDmxDataExist = True
            DataDmx.append([])
            DataDmx[-1].append(index)
            for _param in item['OutputParam']:
                DataDmx[-1].append(_param)
            
            #print(str(index)+"item:"+item['OutputType']) 
    print("DMX:") 
    print(DataDmx) 
     
def GetLocalIp(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    MyLocalIp = s.getsockname()[0]
    #print(MyLocalIp)
    s.close()
    return MyLocalIp

def GetLocalOscPort(): 
    return 2346