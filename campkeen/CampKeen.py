import re

class CampKeenConnector():
    def __init__(self):
        self.HoldingTanks = {
            'Sewage':None,
            'Grey':None
            }

        self.LPGState = None
        self.WaterTankState = None
        self.WaterSourceState = None
        self.WaterState = None
        self.WaterPumpSenseState = None
        self.WarningState = None
        self.AlarmState = None

        self.GeneratorStates = {
            'Fuel Pressure':None,
            'Enclosure Temp':None,
            'Left Head Temp':None,
            'Right Head Temp':None,
        }

        self.BatteryVoltages = {
            'RTC':None,
            'Camper':None
            }

        self.Temps = {
            'Unit':None,
            'Front AC':None,
            'Back AC':None,
            'Outside':None,
            'Back Cabin':None,
            'Hallway':None,
            'Freezer':None,
            'Fridge':None,
            'Bathroom':None,
            'Front Cabin':None,
            }

        self.EnergyMonitorStates = {
            'AC Votlage':None,
            'Power Factor': None, 
            'AC Current':None,
            'AC Frequency':None,
            'Watts':None,
            'Reactive(var)':None,
            'Apparent(VA)':None,
            'Fundimental(W)':None, 
            'Harmonic(W)':None,
            'Real(W)':None,
            }

        self.EnergyMonitorSettingStates = {
            'ACLEGS':None,
            'ACCT1GAIN':None,
            'ACCT2GAIN':None,
            'ACVOLTAGEGAIN':None,
            'ACFREQ':None,
            'ACPGAGAIN':None,
            }

        self.SystemSettingStates = {
            'AC Energy Monitoring':None,
            'Water Pump Sense On Boot':None,
            'AC Monitoring on Boot': None,
            'Streaming On RS232 On Boot':None,
            'Streaming On USB On Boot':None,
            'Water Duration':None,
            }

        self.Regex = {
            'Sewage':                   {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),Sewage\,(Empty|1\/4|1\/2|3\/4|Full|ERROR Check Tank:\d{4})\r'),  'Function':None, 'Query':None},
            'Grey':                     {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),Grey\,(Empty|1\/4|1\/2|3\/4|Full|ERROR Check Tank:\d{4})\r'),    'Function':None, 'Query':None},
            'LPG':                      {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),LPG\,(\d{,3}|ERROR Check Tank Sensor)\r'),     'Function':None, 'Query':None},
            'Water Source':             {'Regex':re.compile('\%R\,Water Source\,(City|Tank)\r'),                                                                                         'Function':None, 'Query':None},
            'Water Tank':               {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),Water Tank Level\,(Empty|1\/4|1\/2|3\/4|Full|EXTRA FULL)\r'),     'Function':None, 'Query':None},
            'WaterState':               {'Regex':re.compile('\%R\,Water,(On|Off)\r'),                                                                                                    'Function':None, 'Query':None},
            'Pump Sense':               {'Regex':re.compile('\%R\,WaterPumpSense,(On|Off)\r'),  
            'Camper Voltage':           {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),Camper VDC,()\r'),  'Function':None, 'Query':None}, 
            'RTC Voltage':              {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),RTCBattery,()\r'),  'Function':None, 'Query':None},   
            'Units':                    {'Regex':re.compile('\%R\,Units,(I|M)\r'),  'Function':None, 'Query':None},
            'Head Unit':                {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),Head Unit Temp,Units,(C|F),(.*)\r'),  'Function':None, 'Query':None},                                                                                      'Function':None, 'Query':None},
            'Generator':                {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),Generator Fuel Pressure,Units,(KPa|PSI),(.*),Generator Temps,Units,(C|F),Enclosure,(.*),Right Head Temp,(.*),Left Head Temp,(.*)\r'),  'Function':None, 'Query':None},
            'NTCTemps':                 {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),NTC Tempetatures,Units,(C|F),Front AC Temp,(.*),Back AC Temp,(.*),Under Awning Temp,(.*),Back Cabin Temp,(.*),Hallway Temp,(.*),Freezer,(.*),Fridge,(.*),Bathroom Temp,(.*)\r'),  'Function':None, 'Query':None},
            'DeviceInfo':               {'Regex':re.compile('\%R\,CampKeen,FW,(.*)\r'),  'Function':None, 'Query':None},
            'AC Energy Monitoring':     {'Regex':re.compile('\%R\,AC Energy Monitoring,(On|Off)\r'),  'Function':None, 'Query':None},
            #'ACVOLTAGEGAIN':            {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None, 'Query':None},
            #'ACFREQ':                   {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None, 'Query':None},
            #'ACPGAGAIN':                {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None, 'Query':None},
            #'ACLEGS':                   {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None, 'Query':None},
            #'ACCT1GAIN':                {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None, 'Query':None},
            #'ACCT2GAIN':                {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None, 'Query':None},
            #'Water Duration': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None, 'Query':None},
            #'Streaming On Boot': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None, 'Query':None},
            #'Water Pump Sense On Boot': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None, 'Query':None},
            #'Energy Mon On Boot': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None, 'Query':None},
            #'Energy': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None, 'Query':None},


            #'Warning':                  {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None},
            #'Alarm':                    {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None},
            
            #'': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),  'Function':None, 'Query':None},

             }


    def IncomingDataParse(self,Buffer):
        for Key in self.Regex:
            result = re.search(self.Regex[Key]['Regex'],Buffer)
            PostProcessFunction = self.Regex[Key]['Function']
            if result:
                if PostProcessFunction == None:
                    print('Found', result)
                else:
                    print('post process',result)

    def NTCTempParse(self,DATA):
        pass

    def HoldingTankParse(self,DATA):
        pass

    def LPGParse(self,DATA):
        pass

    def WaterSourceParse(self):
        pass

test = CampKeenConnector()
test.IncomingDataParse('%R,12:35:55-8/3/2022,Sewage,Empty')