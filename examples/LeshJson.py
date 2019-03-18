import json
import socket

def ReadJsonFile():
    input_file = open ('config/StationSetup.json')
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
            print("We found RuleList():"+GetLocalIp())
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
    print(DataWs) 
         
        
DataDmx = [] 
def InitDataDmx(_ruleList): 
    global DataDmx
    
    
     
def GetLocalIp(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    MyLocalIp = s.getsockname()[0]
    #print(MyLocalIp)
    s.close()
    return MyLocalIp

def GetLocalOscPort(): 
    return 2346