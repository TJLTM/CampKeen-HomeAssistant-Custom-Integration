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
            'Sewage':                   {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),Sewage\,(Empty|1\/4|1\/2|3\/4|Full|ERROR Check Tank:\d{4})\r'),  'Location':self.HoldingTanks['Sewage'], 'Function':None},
            'Grey':                     {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),Grey\,(Empty|1\/4|1\/2|3\/4|Full|ERROR Check Tank:\d{4})\r'),    'Location':self.HoldingTanks['Grey'], 'Function':None},
            'LPG':                      {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),LPG\,(Empty|1\/4|1\/2|3\/4|Full|ERROR Check Tank Sensor)\r'),    'Location':self.LPGState, 'Function':None},
            'Water Source':             {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),Water Source\,(City|Tank)\r'),                                   'Location':self.WaterSourceState, 'Function':None},
            'Water Tank':               {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),Water Tank Level\,(Empty|1\/4|1\/2|3\/4|Full|EXTRA FULL)\r'),    'Location':self.WaterTankState , 'Function':None},
            'WaterState':               {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),Water,(On|Off)\r'),'Location':self.WaterState, 'Function':None},
            'Pump Sense':               {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),WaterPumpSense,(On|Off)\r'),'Location':self.WaterPumpSenseState, 'Function':None},
            #'Warning':                  {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'Alarm':                    {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'EnergyMonitoring':         {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            'NTCTemps':                 {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),NTC Tempetatures,Units,(C|F),Front AC Temp,(.*),Back AC Temp,(.*),Under Awning Temp,(.*),Back Cabin Temp,(.*),Hallway Temp,(.*),Freezer,(.*),Fridge,(.*),Bathroom Temp,(.*)\r'),'Location':'', 'Function':None},
            #'ACLEGS': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'ACCT1GAIN': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'ACCT2GAIN': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'ACVOLTAGEGAIN': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'ACFREQ': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'ACPGAGAIN': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'AC Energy Monitoring': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'Water Pump Sense On Boot': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'Streaming On Boot': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
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