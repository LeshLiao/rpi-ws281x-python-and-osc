import json
import socket

def ReadJsonFile():
    input_file = open ('config/StationSetup.json')
    json_Data = json.load(input_file)
    print("ProjectName:" +json_Data['ProjectName'])
    json_array = json_Data['MyStations']
    #global CurrentRuleList
    CurrentRuleList = []
    
    for item in json_array:
        print("IP:" + item['IP'])
        print("Port:" + str(item['Port']))
        if(GetLocalIp() == item['IP']):
            CurrentRuleList = item['Rules']
            print("We found RuleList():"+GetLocalIp())
            break
    
    InitDataWs(CurrentRuleList)
    InitDataDmx(CurrentRuleList)

    
DataWs = []
def InitDataWs(_ruleList): 
    global DataWs    
    index = 0
    for _rule in _ruleList:
        if(_rule['OutputType'] == "WS281X"):
            DataWs.append([])
            DataWs[-1].append(index)
            for _param in _rule['OutputParam']:
                DataWs[-1].append(_param)
            
            #print(str(index)+"_rule:"+_rule['OutputType']) 
            index += 1
            
    print(DataWs)        
        

def InitDataDmx(_ruleList): 
    DataDmx = [] 
    
    
     
def GetLocalIp(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    MyLocalIp = s.getsockname()[0]
    #print(MyLocalIp)
    s.close()
    return MyLocalIp

def GetLocalOscPort(): 
    return 2346