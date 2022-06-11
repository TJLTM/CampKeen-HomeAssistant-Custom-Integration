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

        self.Regex = {
            'Sewage':                           {'Function':None,                   'DataLocation':self.SewageTankState,           'Query':'\x25SEWAGE?\r'}, #done
            'Grey':                             {'Function':None,                   'DataLocation':self.GreyTankState,             'Query':'\x25GREY?'}, #done
            'LPG':                              {'Function':None,                   'DataLocation':self.LPGState,                  'Query':'\x25LPG?\r'}, #done
            
            'Water Source':                     {'Function':None,                   'DataLocation':self.WaterSourceState,          'Query':'\x25WATERSOURCE?\r'}, #done
            'Water Source Override':            {'Function':None,                   'DataLocation':self.WaterSourceOverRide,       'Query':'\x25WATERSOURCEOVERRIDE?\r'},#done
            'Water Source Override On Boot':    {'Function':None,                   'DataLocation':self.WaterSourceOverrideOnBoot, 'Query':'\x25WATERSOURCEOVERRIDEONBOOT?\r'},#done
            'Water Tank Level':                 {'Function':None,                   'DataLocation':self.WaterTankState,            'Query':'\x25WATERLEVEL?\r'}, #done
            'Water':                            {'Function':None,                   'DataLocation':self.WaterState,                'Query':'\x25WATER?\r'}, #done
            'Water Pump Sense':                 {'Function':None,                   'DataLocation':self.WaterPumpSenseState,       'Query':'\x25WATERPUMPSENSE?\r'},  #done
            'Water Pump Sense on boot':         {'Function':None,                   'DataLocation':self.WaterPumpSenseOnBoot,      'Query':'\x25WATERPUMPSENSEONBOOT?\r'}, #done
            'WATERDURATION':                    {'Function':None,                   'DataLocation':self.WaterDuration,             'Query':'\x25WATERDURATION?\r'},
            
            'Camper VDC':                       {'Function':None,                   'DataLocation':self.CamperBatteryVoltage,      'Query':'\x25BATTERY?\r'}, #done
            'RTCBattery':                       {'Function':None,                   'DataLocation':self.RTCBatteryVoltage,         'Query':'\x25RTCBATTERY?\r'}, #done
            'Head Unit Temp':                   {'Function':self.TempParse,         'DataLocation':None,                           'Query':'\x25UNITTEMP?\r'}, #done
            'NTC Tempetatures':                 {'Function':self.TempParse,         'DataLocation':None,                           'Query':'\x25TEMPS?\r'}, #done

            'Generator Fuel Pressure':          {'Function':self.GeneratorParse,    'DataLocation':None,                           'Query':'\x25GENERATOR?\r'}, #done

            'AC Energy Monitoring':             {'Function':None,                   'DataLocation':self.ACEnergyMonitoring,         'Query':None}, #done
            'AC Energy Monitoring on boot':     {'Function':None,                   'DataLocation':self.ACMonitoringonBoot,         'Query':None}, #done
            'Energy Monitor':                   {'Function':self.EnergyParse,       'DataLocation':None,                            'Query':None}, #done
            'ACVOLTAGEGAIN':                    {'Function':None,                   'DataLocation':self.ACVOLTAGEGAIN,              'Query':'\x25ACVOLTAGEGAIN?\r'}, #done
            'ACFREQ':                           {'Function':None,                   'DataLocation':self.ACFREQ,                     'Query':'\x25ACFREQ?\r'}, #done
            'ACPGAGAIN':                        {'Function':None,                   'DataLocation':self.ACPGAGAIN,                  'Query':'\x25ACPGAGAIN?\r'}, #done
            'ACLEGS':                           {'Function':None,                   'DataLocation':self.ACLEGS,                     'Query':'\x25ACLEGS?\r'}, #done
            'ACCT1GAIN':                        {'Function':None,                   'DataLocation':self.ACCT1GAIN,                  'Query':'\x25ACCT1GAIN?\r'}, #done
            'ACCT2GAIN':                        {'Function':None,                   'DataLocation':self.ACCT2GAIN,                  'Query':'\x25ACCT2GAIN?\r'}, #done

            'StreamingData':                    {'Function':self.StreamingParse,    'DataLocation':None,                            'Query':'\x25STREAMING?\r'}, #done
            'Streaming Data on boot':           {'Function':self.StreamingBootParse,'DataLocation':None,                            'Query':'\x25STREAMINGONBOOT?\r'}, #done
            'Units':                            {'Function':None,                   'DataLocation':self.Units,                      'Query':'\x25UNITS?\r'}, #done
            'CampKeen':                         {'Function':None,                   'DataLocation':self.DeviceInfo,                 'Query':'\x25DEVICE?\r'},#done
            'Warning':                          {'Function':None,                   'DataLocation':self.WarningState,               'Query':'\x25WARNING?\r'}, #done
            'ALARM':                            {'Function':None,                   'DataLocation':self.AlarmState,                 'Query':'\x25ALARM?\r'}, #done
            'Current Port':                     {'Function':None,                   'DataLocation':self.CurrentPort,                'Query':'\x25PORT?\r'}, #done
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
        if Name in self.Regex:
            return self.Regex[Name]['Query']
        else:
            return None

    def SendCommands(self,WhichCommand):
        if WhichCommand == '':
            pass

    def IncomingDataParse(self,Buffer):
        StartTime = time.monotonic()
        while len(Buffer) !=0: 
            IsThereAStartChar = Buffer.find('%R')
            IsThereACR = Buffer.find('\r')
            if IsThereAStartChar != -1 and IsThereACR != -1:
                SliceAndDice = Buffer[IsThereAStartChar:IsThereACR].split(',')

                if len(SliceAndDice) > 1:
                    for key in self.Regex:
                        if SliceAndDice[2] == key and key != 'Units':
                            if self.Regex[key]['Function'] == None:
                                if len(self.Regex[key]['DataLocation']) != 0:
                                    self.Regex[key]['DataLocation'].pop(1)
                                    self.Regex[key]['DataLocation'].pop(0)
                                self.Regex[key]['DataLocation'].insert(0,SliceAndDice[1])
                                self.Regex[key]['DataLocation'].insert(1,SliceAndDice[3])
                            else:
                                self.Regex[key]['Function'](SliceAndDice)
                        elif SliceAndDice[1] == key:
                            if self.Regex[key]['Function'] == None:
                                if len(self.Regex[key]['DataLocation']) != 0:
                                    self.Regex[key]['DataLocation'].pop(1)
                                    self.Regex[key]['DataLocation'].pop(0)
                                self.Regex[key]['DataLocation'].insert(0,None)
                                self.Regex[key]['DataLocation'].insert(1,SliceAndDice[2])
                            else:
                                self.Regex[key]['Function'](SliceAndDice)

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
            self.Temps['Outside'] = [Data[1],Data[10]]
            self.Temps['Back Cabin'] = [Data[1],Data[12]]
            self.Temps['Hallway'] = [Data[1],Data[14]]
            self.Temps['Freezer'] = [Data[1],Data[16]]
            self.Temps['Fridge'] = [Data[1],Data[18]]
            self.Temps['Bathroom'] = [Data[1],Data[20]]
            self.Temps['Front Cabin'] = [Data[1],Data[22]]
        elif Data[2] ==  'Head Unit Temp':
            self.Temps['Head Unit'] = [Data[1],Data[5]]