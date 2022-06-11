import time

class CampKeenDataParsing():
    def __init__(self):
        self.WarningState = [None,None]
        self.AlarmState = [None,None]
        self.StreamingOnRS232OnBoot = [None,None]
        self.StreamingOnUSBOnBoot = [None,None]
        self.WaterSourceOverrideOnBoot = [None,None]
        self.WaterSourceOverRide = [None,None]
        self.StreamOnRS232 = [None,None]
        self.StreamOnUSB = [None,None]
        self.CurrentPort = [None,None]
        self.DeviceInfo = [None,None]
        self.Units = [None,None]
        #Tanks
        self.SewageTankState = [None,None]
        self.GreyTankState = [None,None]
        self.LPGState = [None,None]
        #Water
        self.WaterTankState = [None,None]
        self.WaterSourceState = [None,None]
        self.WaterState = [None,None]
        self.WaterPumpSenseState = [None,None]
        self.WaterPumpSenseOnBoot = [None,None]
        self.WaterDuration = [None,None]
        #Batteries
        self.CamperBatteryVoltage = [None,None]
        self.RTCBatteryVoltage = [None,None]
        #Temps
        self.Temps = {
            'Front AC':[None,None],
            'Back AC':[None,None],
            'Under Awning Temp':[None,None],
            'Back Cabin':[None,None],
            'Hallway':[None,None],
            'Freezer':[None,None],
            'Fridge':[None,None],
            'Bathroom':[None,None],
            'Front Cabin':[None,None],
            'Head Unit': [None,None],
            }
        
        #Energy
        self.Generator = {
            'Fuel Pressure':[None,None],
            'Enclosure Temp':[None,None],
            'Left Head Temp':[None,None],
            'Right Head Temp':[None,None],
        }

        self.EnergyMonitorStates = {
            'AC Votlage':[None,None],
            'Power Factor': [None,None], 
            'AC Current':[None,None],
            'AC Frequency':[None,None],
            'Watts':[None,None],
            'Reactive(var)':[None,None],
            'Apparent(VA)':[None,None],
            'Fundimental(W)':[None,None], 
            'Harmonic(W)':[None,None],
            'Real(W)':[None,None],
            }


        self.ACLEGS = [None,None]
        self.ACCT1GAIN = [None,None]
        self.ACCT2GAIN = [None,None]
        self.ACVOLTAGEGAIN = [None,None]
        self.ACFREQ = [None,None]
        self.ACPGAGAIN = [None,None]
        self.ACEnergyMonitoring = [None,None]
        self.ACMonitoringonBoot = [None,None]

        self.Information = {
            'Sewage':                           {'Function':None,                   'DataLocation':self.SewageTankState,           'Query':'\x25SEWAGE?\r'},
            'Grey':                             {'Function':None,                   'DataLocation':self.GreyTankState,             'Query':'\x25GREY?'}, 
            'LPG':                              {'Function':None,                   'DataLocation':self.LPGState,                  'Query':'\x25LPG?\r'}, 
            
            'Water Source':                     {'Function':None,                   'DataLocation':self.WaterSourceState,          'Query':'\x25WATERSOURCE?\r',
                                                 'SetCommand':'SETWATERSOURCE',     'Parameters':None,                             'States':['CITY','TANK']}, 
            'Water Source Override':            {'Function':None,                   'DataLocation':self.WaterSourceOverRide,       'Query':'\x25WATERSOURCEOVERRIDE?\r',
                                                 'SetCommand':'SETWATERSOURCEOVERRIDE', 'Parameters':None,'                         States':['ON', 'OFF']},
            'Water Source Override On Boot':    {'Function':None,                   'DataLocation':self.WaterSourceOverrideOnBoot, 'Query':'\x25WATERSOURCEOVERRIDEONBOOT?\r'},
            'Water Tank Level':                 {'Function':None,                   'DataLocation':self.WaterTankState,            'Query':'\x25WATERLEVEL?\r'}, 
            'Water':                            {'Function':None,                   'DataLocation':self.WaterState,                'Query':'\x25WATER?\r',
                                                 'SetCommand':'WATER',              'Parameters':None,                              'States':['ON', 'OFF']}, 
            'Water Pump Sense':                 {'Function':None,                   'DataLocation':self.WaterPumpSenseState,       'Query':'\x25WATERPUMPSENSE?\r',
                                                 'SetCommand':'SETWATERPUMPSENSE',  'Parameters':None,                              'States':['ON', 'OFF']},  
            'Water Pump Sense on boot':         {'Function':None,                   'DataLocation':self.WaterPumpSenseOnBoot,      'Query':'\x25WATERPUMPSENSEONBOOT?\r'}, 
            'WATERDURATION':                    {'Function':None,                   'DataLocation':self.WaterDuration,             'Query':'\x25WATERDURATION?\r'},
            'Camper VDC':                       {'Function':None,                   'DataLocation':self.CamperBatteryVoltage,      'Query':'\x25BATTERY?\r'}, 
            'RTCBattery':                       {'Function':None,                   'DataLocation':self.RTCBatteryVoltage,         'Query':'\x25RTCBATTERY?\r'}, 
            'Head Unit Temp':                   {'Function':self.TempParse,         'DataLocation':None,                           'Query':'\x25UNITTEMP?\r'}, 
            'NTC Tempetatures':                 {'Function':self.TempParse,         'DataLocation':None,                           'Query':'\x25TEMPS?\r'}, 

            'Generator Fuel Pressure':          {'Function':self.GeneratorParse,    'DataLocation':None,                           'Query':'\x25GENERATOR?\r'}, 

            'AC Energy Monitoring':             {'Function':None,                   'DataLocation':self.ACEnergyMonitoring,         'Query':'\x25ACENMON?\r',
                                                 'SetCommand':'SETACENMON',         'Parameters':None,                              'States':['ON', 'OFF']}, 
            'AC Energy Monitoring on boot':     {'Function':None,                   'DataLocation':self.ACMonitoringonBoot,         'Query':'\x25ACENMONONBOOT?\r'}, 
            'Energy Monitor':                   {'Function':self.EnergyParse,       'DataLocation':None,                            'Query':'\x25ENERGY?\r',}, 
            'ACVOLTAGEGAIN':                    {'Function':None,                   'DataLocation':self.ACVOLTAGEGAIN,              'Query':'\x25ACVOLTAGEGAIN?\r'}, 
            'ACFREQ':                           {'Function':None,                   'DataLocation':self.ACFREQ,                     'Query':'\x25ACFREQ?\r'}, 
            'ACPGAGAIN':                        {'Function':None,                   'DataLocation':self.ACPGAGAIN,                  'Query':'\x25ACPGAGAIN?\r'}, 
            'ACLEGS':                           {'Function':None,                   'DataLocation':self.ACLEGS,                     'Query':'\x25ACLEGS?\r'}, 
            'ACCT1GAIN':                        {'Function':None,                   'DataLocation':self.ACCT1GAIN,                  'Query':'\x25ACCT1GAIN?\r'}, 
            'ACCT2GAIN':                        {'Function':None,                   'DataLocation':self.ACCT2GAIN,                  'Query':'\x25ACCT2GAIN?\r'}, 

            'StreamingData':                    {'Function':self.StreamingParse,    'DataLocation':None,                            'Query':'\x25STREAMING?\r',
                                                 'SetCommand':'SETSTREAMINGDATA',   'Parameters':['USB','RS232'],                   'States':['ON', 'OFF']}, 
            'Streaming Data on boot':           {'Function':self.StreamingBootParse,'DataLocation':None,                            'Query':'\x25STREAMINGONBOOT?\r'}, 
            'Units':                            {'Function':None,                   'DataLocation':self.Units,                      'Query':'\x25UNITS?\r'}, 
            'CampKeen':                         {'Function':None,                   'DataLocation':self.DeviceInfo,                 'Query':'\x25DEVICE?\r'},
            'Warning':                          {'Function':None,                   'DataLocation':self.WarningState,               'Query':'\x25WARNING?\r',
                                                 'SetCommand':'RESETWARNINGS',      'Parameters':None,                              'States':None}, 
            'ALARM':                            {'Function':None,                   'DataLocation':self.AlarmState,                 'Query':'\x25ALARM?\r',
                                                 'SetCommand':'RESETALLALARMS',     'Parameters':None,                              'States':None}, 
            'Current Port':                     {'Function':None,                   'DataLocation':self.CurrentPort,                'Query':'\x25PORT?\r'}, 
             }

    def GetState(self,Name):
        WhatToReturn = [None, None]
        if Name in self.Information:
            if self.Information[Name]['DataLocation'] != None:
                WhatToReturn = self.Information[Name]['DataLocation']
            else:
                pass
        return WhatToReturn
        
    def Query(self,Name):
        if Name in self.Information:
            return self.Information[Name]['Query']
        else:
            return None

    def SetCommands(self,WhichCommand):
        if WhichCommand in self.Information:
            if 'SetCommand' in self.Information[WhichCommand].keys():
                return {'Command':self.Information[WhichCommand]['SetCommand'],'Parameters':self.Information[WhichCommand]['Parameters'],'States':self.Information[WhichCommand]['States']}
            else:
                return {}
        else:
            return {}

    def IncomingDataParse(self,Buffer):
        StartTime = time.monotonic()
        while len(Buffer) !=0: 
            IsThereAStartChar = Buffer.find('%R')
            IsThereACR = Buffer.find('\r')
            if IsThereAStartChar != -1 and IsThereACR != -1:
                SliceAndDice = Buffer[IsThereAStartChar:IsThereACR].split(',')

                if len(SliceAndDice) > 1:
                    for key in self.Information:
                        if SliceAndDice[2] == key and key != 'Units':
                            if self.Information[key]['Function'] == None:
                                if len(self.Information[key]['DataLocation']) != 0:
                                    self.Information[key]['DataLocation'].pop(1)
                                    self.Information[key]['DataLocation'].pop(0)
                                self.Information[key]['DataLocation'].insert(0,SliceAndDice[1])
                                self.Information[key]['DataLocation'].insert(1,SliceAndDice[3])
                            else:
                                self.Information[key]['Function'](SliceAndDice)
                        elif SliceAndDice[1] == key:
                            if self.Information[key]['Function'] == None:
                                if len(self.Information[key]['DataLocation']) != 0:
                                    self.Information[key]['DataLocation'].pop(1)
                                    self.Information[key]['DataLocation'].pop(0)
                                self.Information[key]['DataLocation'].insert(0,None)
                                self.Information[key]['DataLocation'].insert(1,SliceAndDice[2])
                            else:
                                self.Information[key]['Function'](SliceAndDice)

            if IsThereAStartChar == -1 and len(Buffer) != 0:
                #case of junk in the buffer
                Buffer = ''
            else:
                if IsThereACR > IsThereAStartChar:
                    Buffer = Buffer[IsThereACR:]
                else:
                    Buffer = Buffer[IsThereAStartChar:]

            Duration = abs(StartTime-time.monotonic())
            if Duration > 0.5:
                break

        return Buffer

    def StreamingParse(self,Data):
        self.StreamOnRS232 = [None,Data[5]]
        self.StreamOnUSB = [None,Data[3]]

    def StreamingBootParse(self,Data):
        self.StreamingOnRS232OnBoot = [None,Data[5]]
        self.StreamingOnUSBOnBoot = [None,Data[3]]

    def GeneratorParse(self,Data):
        self.Generator['Fuel Pressure'] = [Data[1],Data[5]]
        self.Generator['Enclosure Temp'] = [Data[1],Data[10]]
        self.Generator['Right Head Temp'] = [Data[1],Data[12]]
        self.Generator['Left Head Temp'] = [Data[1],Data[14]]

    def EnergyParse(self, Data):
        self.EnergyMonitorStates['AC Votlage'] = [Data[1],Data[3]]
        self.EnergyMonitorStates['AC Current'] = [Data[1],Data[5]]
        self.EnergyMonitorStates['Power Factor'] = [Data[1],Data[7]]
        self.EnergyMonitorStates['Real(W)'] = [Data[1],Data[9]]
        self.EnergyMonitorStates['AC Frequency'] = [Data[1],Data[11]]
        self.EnergyMonitorStates['Watts'] = [Data[1],Data[13]]
        self.EnergyMonitorStates['Reactive(var)'] = [Data[1],Data[15]]
        self.EnergyMonitorStates['Apparent(VA)'] = [Data[1],Data[17]]
        self.EnergyMonitorStates['Fundimental(W)'] = [Data[1],Data[19]]
        self.EnergyMonitorStates['Harmonic(W)'] = [Data[1],Data[21]]    

    def TempParse(self,Data):
        if Data[2] ==  'NTC Tempetatures':
            self.Temps['Front AC'] = [Data[1],Data[6]]
            self.Temps['Back AC'] = [Data[1],Data[8]]
            self.Temps['Under Awning Temp'] = [Data[1],Data[10]]
            self.Temps['Back Cabin'] = [Data[1],Data[12]]
            self.Temps['Hallway'] = [Data[1],Data[14]]
            self.Temps['Freezer'] = [Data[1],Data[16]]
            self.Temps['Fridge'] = [Data[1],Data[18]]
            self.Temps['Bathroom'] = [Data[1],Data[20]]
            self.Temps['Front Cabin'] = [Data[1],Data[22]]
        elif Data[2] ==  'Head Unit Temp':
            self.Temps['Head Unit'] = [Data[1],Data[5]]