import time

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
            'Under Awning Temp':[],
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
        self.DeviceInfo = []
        self.Units = []

        self.Regex = {
            'Sewage':                   {'Function':None,                   'DataLocation':self.SewageTankState,           'Query':'\x25SEWAGE?\r'}, #done
            'Grey':                     {'Function':None,                   'DataLocation':self.GreyTankState,             'Query':'\x25GREY?'}, #done
            'LPG':                      {'Function':None,                   'DataLocation':self.LPGState,                  'Query':'\x25LPG?\r'}, #done
            
            'Water Source':             {'Function':None,                   'DataLocation':self.WaterSourceState,          'Query':'\x25WATERSOURCE?\r'}, #done
            'Water Tank Level':         {'Function':None,                   'DataLocation':self.WaterTankState,            'Query':'\x25WATERLEVEL?\r'}, #done
            'Water':                    {'Function':None,                   'DataLocation':self.WaterState,                'Query':'\x25WATER?\r'}, #done
            'Water Pump Sense':         {'Function':None,                   'DataLocation':self.WaterPumpSenseState,       'Query':'\x25WATERPUMPSENSE?\r'},  #done
            'Water Pump Sense on boot': {'Function':None,                   'DataLocation':self.WaterPumpSenseOnBoot,      'Query':'\x25WATERPUMPSENSEONBOOT?\r'}, #done
            'WATERDURATION':            {'Function':self.WaterDurationParse,'DataLocation':self.WaterDuration,             'Query':'\x25WATERDURATION?\r'},
            
            'Camper VDC':               {'Function':None,                   'DataLocation':self.CamperBatteryVoltage,      'Query':'\x25BATTERY?\r'}, #done
            'RTCBattery':               {'Function':None,                   'DataLocation':self.RTCBatteryVoltage,         'Query':'\x25RTCBATTERY?\r'}, #done
            'Head Unit Temp':           {'Function':self.TempParse,         'DataLocation':None,                           'Query':'\x25UNITTEMP?\r'}, #done
            'NTC Tempetatures':         {'Function':self.TempParse,         'DataLocation':None,                           'Query':'\x25TEMPS?\r'}, #done

            'Generator Fuel Pressure':  {'Function':self.GeneratorParse,    'DataLocation':None,                           'Query':'\x25GENERATOR?\r'}, #done

            'AC Energy Monitoring':     {'Function':None,                   'DataLocation':self.ACEnergyMonitoring,         'Query':None}, #done
            'AC Energy Monitoring on boot':{'Function':None,                'DataLocation':self.ACMonitoringonBoot,         'Query':None}, #done
            'Energy Monitor':           {'Function':self.EnergyParse,       'DataLocation':None,                            'Query':None}, #done
            'ACVOLTAGEGAIN':            {'Function':None,                   'DataLocation':self.ACVOLTAGEGAIN,              'Query':'\x25ACVOLTAGEGAIN?\r'}, #done
            'ACFREQ':                   {'Function':None,                   'DataLocation':self.ACFREQ,                     'Query':'\x25ACFREQ?\r'}, #done
            'ACPGAGAIN':                {'Function':None,                   'DataLocation':self.ACPGAGAIN,                  'Query':'\x25ACPGAGAIN?\r'}, #done
            'ACLEGS':                   {'Function':None,                   'DataLocation':self.ACLEGS,                     'Query':'\x25ACLEGS?\r'}, #done
            'ACCT1GAIN':                {'Function':None,                   'DataLocation':self.ACCT1GAIN,                  'Query':'\x25ACCT1GAIN?\r'}, #done
            'ACCT2GAIN':                {'Function':None,                   'DataLocation':self.ACCT2GAIN,                  'Query':'\x25ACCT2GAIN?\r'}, #done

            'StreamingData':            {'Function':self.StreamingParse,    'DataLocation':None,                            'Query':'\x25STREAMINGONBOOT?\r'}, #done
            'Units':                    {'Function':None,                   'DataLocation':self.Units,                      'Query':'\x25UNITS?\r'}, 
            'DeviceInfo':               {'Function':None,                   'DataLocation':self.DeviceInfo,                 'Query':'\x25DEVICE?\r'},
            'Warning':                  {'Function':self.WarningParse,      'DataLocation':None,                            'Query':'\x25WARNING?\r'},
            'Port':                     {'Function':None,                   'DataLocation':self.CurrentPort,                'Query':'\x25PORT?\r'},
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
        StartTime = time.monotonic()
        while len(Buffer) !=0: 
            IsThereAStartChar = Buffer.find('%R')
            IsThereACR = Buffer.find('\r')

            SliceAndDice = Buffer[IsThereAStartChar:IsThereACR].split(',')
            print(SliceAndDice,len(SliceAndDice))
            if len(SliceAndDice) > 1:
                print(SliceAndDice[2],SliceAndDice[1])
                for key in self.Regex:
                    if SliceAndDice[2] == key and key != 'Units':
                        if self.Regex[key]['Function'] == None:
                            self.Regex[key]['DataLocation'].insert(0,SliceAndDice[1])
                            self.Regex[key]['DataLocation'].insert(1,SliceAndDice[3])
                        else:
                            self.Regex[key]['Function'](SliceAndDice)
                    elif SliceAndDice[1] == key:
                        if self.Regex[key]['Function'] == None:
                            self.Regex[key]['DataLocation'].insert(0,None)
                            self.Regex[key]['DataLocation'].insert(1,SliceAndDice[2])

            if IsThereAStartChar == -1 and len(Buffer) != 0:
                #case of junk in the buffer
                Buffer = ''
            else:
                if IsThereACR > IsThereAStartChar:
                    Buffer = Buffer[IsThereACR:]
                else:
                    Buffer = Buffer[IsThereAStartChar:]

            Duration = abs(StartTime-time.monotonic())
            if Duration > 0.1:
                break

        return Buffer

    def WarningParse(self,Data):
        pass

    def WaterDurationParse(self,Data):
        self.WaterDuration = [None,Data[5]]

    def StreamingParse(self,Data):
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
            




Something = '''%R,CampKeen,FW,1.0.9\r
%R,System Time,08:23:00-22/05/2022\r
%R,Warning,None\r
%R,StreamingData,USB,Off,RS232,Off\r
%R,Water Pump Sense,Off\r
%R,AC Energy Monitoring,On\r
%R,Water,Off\r
%R,Units,I\r
%R,Water Source,Tank\r
%R,08:20:33-22/05/2022,Water Tank Level,Full\r
%R,WATERDURATION,Units,Seconds,150\r
%R,08:20:32-22/05/2022,Sewage,1/2\r
%R,08:20:30-22/05/2022,Grey,1/4\r
%R,08:20:33-22/05/2022,LPG,97\r
%R,08:20:32-22/05/2022,Camper VDC,13.27\r
%R,08:20:32-22/05/2022,RTCBattery,2.90\r
%R,08:22:58-22/05/2022,NTC Tempetatures,Units,F,Front AC Temp,59.94,Back AC Temp,61.01,Under Awning Temp,59.76,Back Cabin Temp,60.83,Hallway Temp,60.47,Freezer,-19.70,Fridge,45.46,Bathroom Temp,60.30,Front Cabin Temp,61.54\r
%R,08:23:00-22/05/2022,Head Unit Temp,Units,F,70.70\r
%R,08:22:58-22/05/2022,Generator Fuel Pressure,Units,PSI,0.00,Generator Temps, Enclosure,Units,F,54.98,Right Head Temp,56.74,Left Head Temp,57.77\r
%R,08:22:51-22/05/2022,Energy Monitor,119.40,V,4.18,A,0.96,PF,8.36,W{real),60.00,Hz,249.74,W(total),1.59,var(reactive),-1.80,VA(apparent),9.96,W(fundimental),-1.60,W(harmonic)\r
%R,ACVOLTAGEGAIN,1960\r
%R,ACFREQ,60\r
%R,ACPGAGAIN,57005\r
%R,ACLEGS,1\r
%R,ACCT1GAIN,49320\r
%R,ACCT2GAIN,1\r
%R,Streaming Data on boot,USB,Off,RS232,Off\r
%R,StreamingData,USB,Off,RS232,Off\r
%R,AC Energy Monitoring on boot,On\r
%R,Water Pump Sense on boot,Off\r
'''

test = CampKeenDataParsing()
print('Returned Buffer', test.IncomingDataParse(Something))

print('SewageTankState',test.SewageTankState)
print('GreyTankState',test.GreyTankState)
print('LPGState',test.LPGState)
print('WaterTankState',test.WaterTankState)
print('WaterSourceState',test.WaterSourceState)
print('WaterState',test.WaterState)
print('WaterPumpSenseState',test.WaterPumpSenseState)
print('WaterPumpSenseOnBoot',test.WaterPumpSenseOnBoot)
print('WaterDuration',test.WaterDuration)

print('CamperBatteryVoltage',test.CamperBatteryVoltage)
print('RTCBatteryVoltage',test.RTCBatteryVoltage)

print('Generator',test.Generator)
print('EnergyMonitorStates',test.EnergyMonitorStates)
print('Temps',test.Temps)

print('ACLEGS',test.ACLEGS)
print('ACCT1GAIN',test.ACCT1GAIN)
print('ACCT2GAIN',test.ACCT2GAIN)
print('ACVOLTAGEGAIN',test.ACVOLTAGEGAIN)
print('ACFREQ',test.ACFREQ)
print('ACPGAGAIN',test.ACPGAGAIN)
print('ACEnergyMonitoring',test.ACEnergyMonitoring)
print('ACMonitoringonBoot',test.ACMonitoringonBoot)

print('StreamingOnRS232OnBoot',test.StreamingOnRS232OnBoot)
print('StreamingOnUSBOnBoot',test.StreamingOnUSBOnBoot)
print('CurrentPort',test.CurrentPort)
print('DeviceInfo',test.DeviceInfo)
print('Units',test.Units)
