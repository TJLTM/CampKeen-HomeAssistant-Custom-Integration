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
            'LPG':                      {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),LPG\,(Empty|1\/4|1\/2|3\/4|Full|ERROR Check Tank Sensor)\r'),    'Location':'', 'Function':None},
            'Water Source':             {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),Water Source\,(City|Tank)\r'),                                   'Location':'', 'Function':None},
            'Water Tank':               {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),Water Tank Level\,(Empty|1\/4|1\/2|3\/4|Full|EXTRA FULL)\r'),    'Location':'', 'Function':None},
            'WaterState':               {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            'Pump Sense':               {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            'Warning':                  {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            'Alarm':                    {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            'EnergyMonitoring':         {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            'Temps':                    {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            '': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
            #'': {'Regex':re.compile('\%R\,(\d{1,2}\:\d{1,2}\:\d{1,2}\-\d{1,2}\/\d{1,2}\/\d{4}),'),'Location':'', 'Function':None},
             }


    def IncomingDataParse(self,Buffer):
        for Key in self.Regex:
            result = re.search(self.Regex[Key]['Regex'],Buffer)
            if result:
                print('Found', result)

    def SetWaterState(self,State):
        pass

    
test = CampKeenConnector()
test.IncomingDataParse('%R,12:35:55-8/3/2022,Sewage,Empty')