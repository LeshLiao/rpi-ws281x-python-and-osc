
def init_global_var():
    global myList
    myList = []
    
    global RuleListSize
    RuleListSize = 0
    
    global DmxMaxChannel
    DmxMaxChannel = 0
    
    global IsDmxAvailible
    IsDmxAvailible = False
    
    global IsDmxDataExist
    IsDmxDataExist = False
    
    global DeviceConfigList
    DeviceConfigList = []
    
    global JsonTimestamp
    
    global MyOscPort

a = [[0, 0, 0],
     [33, 33, 33],
     [139, 139, 139],
     [255, 255, 255],
     [255, 95, 92],
     [255, 5, 5],
     [250, 0, 0],
     [36, 6, 6],
     [255, 192, 108],
     [252, 110, 2],
     [115, 32, 5],
     [48, 25, 0],
     [251, 249, 27],
     [252, 246, 3],
     [104, 102, 4],
     [25, 25, 0],
     [139, 247, 50],
     [67, 241, 8],
     [22, 100, 0],
     [14, 52, 0],
     [45, 247, 49],
     [0, 255, 0],
     [0, 100, 0],
     [0, 25, 0],
     [48, 247, 82],
     [0, 247, 1],
     [3, 98, 4],
     [0, 24, 2],
     [40, 251, 138],
     [0, 249, 73],
     [3, 99, 25],
     [0, 32, 17],
     [45, 243, 189],
     [6, 243, 61],
     [0, 106, 60],
     [0, 27, 17],
     [55, 206, 255],
     [1, 184, 250],
     [0, 78, 97],
     [0, 19, 26],
     [78, 152, 255],
     [4, 105, 255],
     [0, 39, 110],
     [0, 4, 36],
     [88, 100, 253],
     [0, 0, 255],
     [3, 16, 105],
     [0, 2, 34],
     [149, 101, 254],
     [100, 54, 251],
     [26, 18, 121],
     [10, 6, 67],
     [255, 106, 254],
     [255, 63, 255],
     [110, 22, 109],
     [36, 2, 35],
     [247, 103, 160],
     [255, 42, 99],
     [110, 11, 32],
     [40, 2, 17],
     [255, 51, 0],
     [172, 69, 1],
     [140, 97, 2],
     [79, 118, 2],
     [3, 68, 1],
     [8, 93, 64],
     [0, 103, 139],
     [3, 51, 255],
     [0, 84, 93],
     [33, 42, 224],
     [139, 139, 137],
     [43, 43, 43],
     [248, 35, 0],
     [197, 247, 0],
     [183, 234, 5],
     [87, 250, 3],
     [5, 145, 4],
     [0, 250, 139],
     [0, 186, 248],
     [11, 56, 255],
     [66, 51, 254],
     [136, 53, 255],
     [198, 46, 143],
     [80, 41, 4],
     [254, 94, 0],
     [144, 226, 1],
     [107, 249, 0],
     [0, 247, 0],
     [0, 248, 0],
     [68, 247, 120],
     [4, 247, 210],
     [95, 154, 255],
     [46, 99, 211],
     [149, 144, 238],
     [221, 62, 255],
     [255, 41, 108],
     [252, 147, 0],
     [197, 186, 0],
     [43, 247, 9],
     [150, 104, 17],
     [70, 54, 0],
     [0, 93, 0],
     [2, 96, 70],
     [17, 22, 42],
     [18, 44, 111],
     [125, 76, 25],
     [181, 27, 1],
     [244, 100, 54],
     [255, 126, 7],
     [255, 227, 0],
     [164, 226, 2],
     [116, 189, 0],
     [33, 35, 60],
     [225, 245, 96],
     [136, 244, 194],
     [168, 169, 255],
     [153, 123, 255],
     [77, 77, 77],
     [134, 134, 134],
     [227, 251, 252],
     [178, 19, 9],
     [66, 2, 2],
     [0, 208, 10],
     [2, 75, 0],
     [197, 186, 0],
     [79, 60, 1],
     [194, 112, 2],
     [89, 28, 3]]


def GetColorByVolume(vol):
    return a[vol][0], a[vol][1], a[vol][2]

