import re

class CampKeenConnector():
    def __init__(self):
        self.RXBuffer = b''

    def Run(self):
        pass

    def Disconnect(self):
        pass

    def Loopy(self):
        pass



class CampKeenDataParsing():
    def __init__(self):
        self.DateTimePattern = '(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4})'
        #time pattern format == 
        self.FloatPattern = '([+-]?([0-9]*[.])?[0-9]+)'

        self.PressureUnit = None
        self.TempetureUnit = None
        self.WarningState = []
        self.AlarmState = []
        #Tanks
        self.SewageTankState = []
        self.GreyTankState = []
        self.LPGState = []
        #Water
        self.WaterTankState = []
        self.WaterSourceState = []
        self.WaterState = []
        self.WaterPumpSenseState = []
        self.WaterPumpSenseOnBoot = []
        self.WaterDuration = []

        self.CamperBatteryVoltage = []
        self.RTCBatteryVoltage = []

        self.Generator = {
            'Fuel Pressure':[],
            'Enclosure Temp':[],
            'Left Head Temp':[],
            'Right Head Temp':[],
        }

        self.Temps = {
            'Front AC':[],
            'Back AC':[],
            'Outside':[],
            'Back Cabin':[],
            'Hallway':[],
            'Freezer':[],
            'Fridge':[],
            'Bathroom':[],
            'Front Cabin':[],
            'Head Unit': [],
            }

        self.EnergyMonitorStates = {
            'AC Votlage':[],
            'Power Factor': [], 
            'AC Current':[],
            'AC Frequency':[],
            'Watts':[],
            'Reactive(var)':[],
            'Apparent(VA)':[],
            'Fundimental(W)':[], 
            'Harmonic(W)':[],
            'Real(W)':[],
            }


        self.ACLEGS = []
        self.ACCT1GAIN = []
        self.ACCT2GAIN = []
        self.ACVOLTAGEGAIN = []
        self.ACFREQ = []
        self.ACPGAGAIN = []
        self.ACEnergyMonitoring = []
        self.ACMonitoringonBoot = []

        self.StreamingOnRS232OnBoot = []
        self.StreamingOnUSBOnBoot = []
        self.CurrentPort = []


        self.Regex = {
            'Sewage':                   {'Regex':re.compile('\%R\,'+ self.DateTimePattern +',Sewage\,(Empty|1\/4|1\/2|3\/4|Full|ERROR Check Tank:\d{4})\r'),        'Function':None, 'DataLocation':self.SewageTankState,           'Query':'\x25SEWAGE?\r'},
            'Grey':                     {'Regex':re.compile('\%R\,'+ self.DateTimePattern +',Grey\,(Empty|1\/4|1\/2|3\/4|Full|ERROR Check Tank:\d{4})\r'),          'Function':None, 'DataLocation':self.GreyTankState,             'Query':'\x25GREY?'},
            'LPG':                      {'Regex':re.compile('\%R\,'+ self.DateTimePattern +',LPG\,(\d{,3}|ERROR Check Tank Sensor)\r'),                             'Function':None, 'DataLocation':self.LPGState,                  'Query':'\x25LPG?\r'},
            
            'Water Source':             {'Regex':re.compile('\%R\,Water Source\,(City|Tank)\r'),                                                                    'Function':None, 'DataLocation':self.WaterSourceState,          'Query':'\x25WATERSOURCE?\r'},
            'Water Tank':               {'Regex':re.compile('\%R\,{0}\,Water Tank Level\,(Empty|1\/4|1\/2|3\/4|Full|EXTRA FULL)\r'.format(self.DateTimePattern)),   'Function':None, 'DataLocation':self.WaterTankState,            'Query':'\x25WATERLEVEL?\r'},
            'WaterState':               {'Regex':re.compile('\%R\,Water\,(On|Off)\r'),                                                                              'Function':None, 'DataLocation':self.WaterState,                'Query':'\x25WATER?\r'},
            'Pump Sense':               {'Regex':re.compile('\%R\,WaterPumpSense\,(On|Off)\r'),                                                                     'Function':None, 'DataLocation':self.WaterPumpSenseState,       'Query':'\x25WATERPUMPSENSE?\r'}, 
            'Water Pump Sense On Boot': {'Regex':re.compile('\%R\,WaterPumpSense on boot\,(On|Off)\r'),                                                             'Function':None, 'DataLocation':self.WaterPumpSenseOnBoot,      'Query':'\x25WATERPUMPSENSEONBOOT?\r'},
            'Water Duration':           {'Regex':re.compile('\%R\,WATERDURATION\,Units\,Seconds\,(\d{3,})\r'),                                                      'Function':None, 'DataLocation':self.WaterDuration,             'Query':'\x25WATERDURATION?\r'},
            
            'Camper Voltage':           {'Regex':re.compile('\%R\,{0}\,Camper VDC\,{0}\r'.format(self.FloatPattern)),                                               'Function':None, 'DataLocation':self.CamperBatteryVoltage,      'Query':'\x25BATTERY?\r'}, 
            'RTC Voltage':              {'Regex':re.compile('\%R\,{0}\,RTCBattery\,{0}\r'.format(self.FloatPattern)),                                               'Function':None, 'DataLocation':self.RTCBatteryVoltage,         'Query':'\x25RTCBATTERY?\r'},   
            'Head Unit':                {'Regex':re.compile('\%R\,{0}\,(Head Unit Temp),Units\,(C|F)\,{1}\r'.format(self.DateTimePattern,self.FloatPattern)),       'Function':self.TempParse, 'DataLocation':None,  'Query':'\x25UNITTEMP?\r'},
            'NTCTemps':                 {'Regex':re.compile('\%R\,{0}\,(NTC Tempetatures),Units\,(C|F)\,Front AC Temp\,({1})\,Back AC Temp\,({1})\,Under Awning Temp\,({1})\,Back Cabin Temp\,({1})\,Hallway Temp\,({1})\,Freezer\,({1})\,Fridge\,({1})\,Bathroom Temp\,({1})\r'.format(self.DateTimePattern,self.FloatPattern)),  'Function':self.TempParse, 'DataLocation':None,  'Query':'\x25TEMPS?\r'},

            'Generator':                {'Regex':re.compile('\%R\,{0}\,Generator Fuel Pressure\,Units\,(KPa|PSI)\,{1}\,Generator Temps\,Units\,(C|F)\,Enclosure\,{1}\,Right Head Temp\,{1}\,Left Head Temp\,{1}\r'.format(self.DateTimePattern,self.FloatPattern)),  'Function':self.GeneratorParse, 'DataLocation':None,  'Query':'\x25GENERATOR?\r'},

            'AC Energy Monitoring':     {'Regex':re.compile('\%R\,AC Energy Monitoring\,(On|Off)\r'),                                                               'Function':None, 'DataLocation':None,  'Query':None},
            'Energy Mon On Boot':       {'Regex':re.compile('\%R\,AC Energy Monitoring on Boot\,(On|Off)\r'),                                                       'Function':None, 'DataLocation':None,  'Query':None},
            'Energy':                   {'Regex':re.compile('\%R\,{0}\,Energy Monitor\,({1})\,V\,({1})\,A\,({1})\,PF\,({1})\,W\(real\)\,({1})\,Hz\,({1})\,W\(total\)\,({1})\,var\(reactive\)\,({1})\,VA\(apparent\)\,({1})\,W\(fundimental\)\,({1})\,W\(harmonic\)\r'.format(self.DateTimePattern,self.FloatPattern)),  'Function':None, 'DataLocation':None,  'Query':None},
            'ACVOLTAGEGAIN':            {'Regex':re.compile('\%R\,ACVOLTAGEGAIN\,(\d{,5})\r'),                                                                      'Function':None, 'DataLocation':None,  'Query':'\x25ACVOLTAGEGAIN?\r'},
            'ACFREQ':                   {'Regex':re.compile('\%R\,ACFREQ\,(60|50)\r'),                                                                              'Function':None, 'DataLocation':None,  'Query':'\x25ACFREQ?\r'},
            'ACPGAGAIN':                {'Regex':re.compile('\%R\,ACPGAGAIN\,(\d{,5})\r'),                                                                          'Function':None, 'DataLocation':None,  'Query':'\x25ACPGAGAIN?\r'},
            'ACLEGS':                   {'Regex':re.compile('\%R\,ACLEGS\,(1|2)\r'),                                                                                'Function':None, 'DataLocation':None,  'Query':'\x25ACLEGS?\r'},
            'ACCT1GAIN':                {'Regex':re.compile('\%R\,ACCT1GAIN\,(\d{,5})\r'),                                                                          'Function':None, 'DataLocation':None,  'Query':'\x25ACCT1GAIN?\r'},
            'ACCT2GAIN':                {'Regex':re.compile('\%R\,ACCT2GAIN\,(\d{,5})\r'),                                                                          'Function':None, 'DataLocation':None,  'Query':'\x25ACCT2GAIN?\r'},

            'Streaming On Boot':        {'Regex':re.compile('\%R\,Streaming Data on boot\,USB\,(On|Off)\,RS232\,(On|Off)\r'),                                       'Function':None, 'DataLocation':None,  'Query':'\x25STREAMINGONBOOT?\r'},
            'Units':                    {'Regex':re.compile('\%R\,Units\,(I|M)\r'),                                                                                 'Function':None, 'DataLocation':None,  'Query':'\x25UNITS?\r'},
            'DeviceInfo':               {'Regex':re.compile('\%R\,CampKeen\,FW\,(.*)\r'),                                                                           'Function':None, 'DataLocation':None,  'Query':'\x25DEVICE?\r'},
            'Warning':                  {'Regex':re.compile('\%R\,{0}\,Warning\,(.*)\r'.format(self.DateTimePattern)),                                              'Function':None, 'DataLocation':None,  'Query':'\x25WARNING?\r'},
            'Port':                     {'Regex':re.compile('\%R\,Current Port\,(RS232|USB)\r'),                                                                    'Function':None, 'DataLocation':None,  'Query':'\x25PORT?\r'},
             }

    def GetState(self,Name):
        WhatToReturn = [None, None]
        if Name in self.Regex.keys():
            if self.Regex[Name]['DataLocation'] != None:
                WhatToReturn = self.Regex[Name]['DataLocation']
            else:
                pass

        return WhatToReturn
        
    def Query(self,Name):
        if Name in self.Regex.keys():
            return self.Regex[Name]['Query']
        else:
            return None

    def SendCommands(self,WhichCommand):
        if WhichCommand == '':
            pass

    def IncomingDataParse(self,Buffer):
        for Key in self.Regex:
            result = re.search(self.Regex[Key]['Regex'],Buffer)
            PostProcessFunction = self.Regex[Key]['Function']
            if result:
                if PostProcessFunction == None:
                    self.Regex[Key]['DataLocation'].append(None)
                    self.Regex[Key]['DataLocation'].append(result.group(1))
                else:
                    self.Regex[Key]['Function'](result)
                Buffer = Buffer[:result.span()[0]] + Buffer[result.span()[1]:]

        IsThereAStartChar = Buffer.find('%R')
        if IsThereAStartChar == -1 and len(Buffer) != 0:
            #case of junk in the buffer
            Buffer = ''
        else:
            if IsThereAStartChar != 0:
                IsThereACR = Buffer.find('\r')
                if IsThereACR > IsThereAStartChar:
                    Buffer = Buffer[IsThereACR:]
                else:
                    Buffer = Buffer[IsThereAStartChar:]

        return Buffer

    def GeneratorParse(self,MatchObj):
        pass

    def EnergyParse(self, MatchObj):
        pass

    def TempParse(self,MatchObj):
        pass



Something = "afsdkl;fu%R,Water,On\r"
test = CampKeenDataParsing()
print(test.WaterState)
print(test.IncomingDataParse(Something))
print(test.WaterState)