# Main file for importing data from devices and parsing them into a list of dicts then finally organizing them into a final common dictionary.
import csv
import xml.etree.ElementTree as ET


class AbbotImport():
    def __init__(self, *args, **kwargs):
        self.abDict= {}
        self.fDict = {}
    def getabbotData(self, fileName):
        with open(fileName, newline='') as csvfile:
          reader = csv.reader(csvfile, delimiter=chr(28), lineterminator=chr(30))
          self.abDict ={rows[1]:rows[2]for rows in reader}
        return self.abDict
    def mode(self, fileName):
        modeclass = AbbotImport()
        mode = modeclass.getabbotData(fileName)
        self.fDict = {
                        'name_given':mode.get('name_given'),
                        'name_family':mode.get('name_family'),
                        'sess_date':mode.get(''),
                        'type':mode.get('type'),
                        'model':mode.get('Device Model Name'),
                        'serial':mode.get('Device Serial Number'),
                        'mode':mode.get('Mode'),
                        'mfg':'Abbot',
                        'lowrate':mode.get('Base Rate'),
                        'max_tracking_rate':mode.get('Maximum Tracking Rate'),
                        'ra_percent_paced':mode.get(''), # ra pacing percentage
                        'rv_percent_paced':mode.get(''), # rv pacing percentage
                        'lv_percent_paced':mode.get(''), # LV pacing percentage
                        'biv_percent_paced':mode.get(''), # biventricular pacing percentage
                        'at_burden':mode.get(''), #at/af burden in pecentage form

                        'ra_sense':mode.get('Atrial Signal Amplitude'),
                        'ra_polarity':mode.get('A Pace Polarity'),
                        'ra_threshold':mode.get('A Amplitude'),
                        'ra_pulsewidth':mode.get('Atrial Pulse Width'),
                        'ra_impedance':mode.get('Atrial Pacing Lead Impedance'),

                        'rv_sense':mode.get('Ventricular Signal Amplitude'),
                        'rv_polarity':mode.get('V Pace Polarity'),
                        'rv_threshold':mode.get('RV. Capture Test Threshold Amplitude'),
                        'rv_pulsewidth':mode.get('RV Pulse Width'),
                        'rv_impedance':mode.get('Ventricular Pacing Lead Impedance'),
                        'hv_impedance':mode.get('HV Lead Impedance'),

                        'lv_sense':mode.get(''),
                        'lv_impedance':mode.get('LV Pacing Lead Impedance'),
                        'lv_amplitude':mode.get('lv_amplitude'),
                        'lv_pulsewidth':mode.get('lv_pulsewidth'),


                        'batt_voltage':mode.get('batt_voltage'),
                        'batt_remaining':mode.get('batt_remaining'),
                        'batt_status':mode.get('Longevity Estimate'),
                        'batt_chrge_time':mode.get('')}
        return self.fDict

class BscImport():
    def __init__(self, *args, **kwargs):
        self.bscDict= {}
        self.fDict = {}
    def getbscData(self, fileName):
        
        with open(fileName, mode='r') as csvfile:
          reader = csv.reader(filter(lambda row: row[0]!='#', csvfile))
          for row in reader:
                k,v = row
                self.bscDict[k]=v
        return self.bscDict
    
    def mode(self, fileName):
        modeclass = BscImport()
        mode = modeclass.getbscData(fileName)
        self.fDict = {'name_given':mode.get('PatientFirstName'),
                        'name_family':mode.get('PatientLastName'),
                        'type':mode.get('SystemTypeTierName'),
                        'model':mode.get('SystemName'),
                        'serial':mode.get('SystemSerialNumber'),
                        'mode':mode.get('BdyNormBradyMode'),
                        'mfg':'Boston Scientific',
                        'lowrate':mode.get('NormParams.LRLIntvl'),
                        'max_tracking':mode.get('Maximum Tracking Rate'),
                        'ra_percent_paced':mode.get(''), # ra pacing percentage
                        'rv_percent_paced':mode.get(''), # rv pacing percentage
                        'lv_percent_paced':mode.get(''), # LV pacing percentage
                        'biv_percent_paced':mode.get(''), # biventricular pacing percentage
                        'at_burden':mode.get(''), #at/af burden in pecentage form

                        'ra_sense':mode.get('ManualIntrinsicResult.RAMsmt.Msmt'),
                        'ra_polarity':mode.get('PaceVectorsParam.RA'),
                        'ra_threshold':mode.get('InterPaceThreshResult.RAMsmt.Amplitude'),
                        'ra_pulsewidth':mode.get('InterPaceThreshResult.RAMsmt.PulseWidth'),
                        'ra_impedance':mode.get('ManualLeadImpedData.RAMsmt.Msmt'),

                        'rv_sense':mode.get('ManualIntrinsicResult.RVMsmt.Msmt'),
                        'rv_polarity':mode.get('PaceVectorsParam.RV'),
                        'rv_threshold':mode.get('InterPaceThreshResult.RVMsmt.Amplitude'),
                        'rv_pulsewidth':mode.get('InterPaceThreshResult.RVMsmt.PulseWidth'),
                        'rv_impedance':mode.get('ManualLeadImpedData.RVMsmt.Msmt'),
                        'hv_impedance':mode.get('ShockImpedanceLastMeas'),

                        'lv_sense':mode.get(''),
                        'lv_impedance':mode.get('ManualLeadImpedData.LVMsmt.Msmt'),
                        'lv_threshold':mode.get('InterPaceThreshResult.LVMsmt.Amplitude'),
                        'lv_pulsewidth':mode.get('InterPaceThreshResult.LVMsmt.PulseWidth'),
                        'lv_polarity':mode.get('PaceVectorsParam.LV'),


                        'batt_voltage':mode.get('batt_voltage'),
                        'batt_remaining':mode.get('batt_remaining'),
                        'batt_status':mode.get('Longevity Estimate'),
                        'batt_chrge_time':mode.get('')}
        return self.fDict
        
class bioImport():

    def __init__(self, *args, **kwargs):
        self.biodevdata = {}
        self.biosessdata = {}
        self.biobatdata = {}
        self.biocapdata = {}
        self.biorvdata = {}
        self.biobradydata = {}
        self.biolist = []
        self.bio_f_dict = {}
        self.bioradata = {}
        self.biohvdata = {}
        self.bioptdata = {}
        self.biolvdata = {}
        self.biodtdata = {}
        self.biostatdata = {}
        self.bioatdata = {}
        self.biocrtdata = {}

    def getBioDevData(self, fileName):
        tree = ET.parse(fileName)
        root = tree.getroot()
        #bioData = {}


        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="DEV"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                            self.biodevdata[keys] = values
        except:
            self.biodevdata = {}


        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="SESS"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                            self.biosessdata[keys] = values
        except:
            self.biosessdata = {}

        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="MSMT"]/section[@name="BATTERY"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                           self. biobatdata[keys] = values
        except:
            self.biobatdata = {}

        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="MSMT"]/section[@name="CAP"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                            self.biocapdata[keys] = values
        except:
            self.biocapdata = {}


        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="MSMT"]/section[@name="LEADCHNL_RV"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                            self.biorvdata[keys] = values
        except:
            self.biorvdata = {}
        
        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="MSMT"]/section[@name="LEADHVCHNL"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                            self.biohvdata[keys] = values
        except:
            self.biohvdata = {}
        

        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="BRADY"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                            self.biobradydata[keys] = values
        except:
            self.biobradydata = {}

        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="AT"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                            self.bioatdata[keys] = values
        except:
            self.bioatdata = {}

        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="CRT"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                            self.biocrtdata[keys] = values
        except:
            self.biocrtdata = {}        
        
        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="MSMT"]/section[@name="LEADCHNL_RA"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                            self.bioradata[keys] = values
        except:
            self.bioradata = {}

        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="MSMT"]/section[@name="LEADCHNL_LV"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                            self.biolvdata[keys] = values
        except:
            self.biolvdata = {}

        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="ATTR"]/section[@name="PT"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                            self.bioptdata[keys] = values
        except:
                self.bioptdata = {}
        
        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="BIO"]/section[@name="REQUEST"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                            self.biodtdata[keys] = values
        except:
                self.biodtdata = {}

        try:
            for child in root.iter("dataset"):
                for x in child.find('.//section[@name="STAT"]'):
                    for a in x.iter('value'):
                        values = a.text
                        keys = a.get('name')
                        for i in keys:
                            self.biostatdata[keys] = values
        except:
            self.biostatydata = {}



        self.biolist.append(self.biobradydata)  #0
        self.biolist.append(self.biorvdata)  #1
        self.biolist.append(self.biocapdata)  #2
        self.biolist.append(self.biosessdata)  #3
        self.biolist.append(self.biodevdata)  #4
        self.biolist.append(self.biobatdata)  #5
        self.biolist.append(self.bioradata)  #6
        self.biolist.append(self.biohvdata)  #7
        self.biolist.append(self.bioptdata)  #8
        self.biolist.append(self.biolvdata)  #9
        self.biolist.append(self.biodtdata) #10
        self.biolist.append(self.biostatdata) #11
        self.biolist.append(self.bioatdata)#12
        self.biolist.append(self.biocrtdata)#13

    def mode(self):
        mode = self.biolist
        self.bio_f_dict = {
        'name_given':mode[8].get('NAME_GIVEN'),
        'name_family':mode[8].get('NAME_FAMILY'),
        'sess_date':mode[10].get('DATE'),
        'type':mode[4].get('TYPE'), # CIED device type
        'model': mode[4].get('MODEL'), # device model name
        'serial': mode[4].get('SERIAL'), # device serial number
        'mode': mode[0].get('MODE'), 
        'mfg':mode[4].get('MFG'), # manufacturer
        'lowrate': mode[0].get('LOWRATE'),
        'ra_percent_paced': mode[11].get('RA_PERCENT_PACED'), # ra pacing percentage
        'rv_percent_paced': mode[11].get('RV_PERCENT_PACED'), # rv pacing percentage
        'lv_percent_paced': mode[11].get('LV_PERCENT_PACED'), # LV pacing percentage
        'biv_percent_paced': mode[13].get('PERCENT_PACED'), # biventricular pacing percentage
        'at_burden': mode[12].get('BURDEN_PERCENT'), #at/af burden in pecentage form
        'max_tracking_rate': mode[0].get('MAX_TRACKING_RATE'),

        'ra_sense': mode[6].get('INTR_AMPL_MEAN'), # ra sensing
        'ra_polarity':mode[6].get('POLARITY'), # ra pacing polarity
        'ra_threshold':mode[6].get('AMPLITUDE'), # ra threshold
        'ra_pulsewidth':mode[6].get('PULSEWIDTH'), # ra threshold pulse width
        'ra_impedance': mode[6].get('VALUE'), 

        'rv_sense': mode[1].get('INTR_AMPL_MEAN'), # rv sensing
        'rv_polarity':mode[1].get('POLARITY'), # rv pacing polarity
        'rv_threshold':mode[1].get('AMPLITUDE'), # rv threshold
        'rv_pulsewidth':mode[1].get('PULSEWIDTH'), # rv threshold pulse width
        'rv_impedance': mode[1].get('VALUE'), # rv impedance measurement
        'hv_impedance':mode[7].get('IMPEDANCE'),  # hv impedance measurement

        'lv_sense': mode[9].get('INTR_AMPL_MEAN'), # lv sensing
        'lv_impedance':mode[9].get('VALUE'), # lv impedance measurement
        'lv_threshold':mode[9].get('AMPLITUDE'), # lv threshold 
        'lv_pulsewidth':mode[9].get('PULSEWIDTH'), # lv threshold pulse width

        'batt_voltage' : mode[5].get('VOLTAGE'), 
        'batt_remaining' : mode[5].get('REMAINING_PERCENTAGE'), # remaining battery percentage
        'batt_status' : mode[5].get('STATUS'),
        'batt_chrge_time' : mode[2].get('CHARGE_TIME')}
        return self.bio_f_dict

class Data():
    def __init__(self, master=None, fileName=None):
        self.master = master
        self.fileName = fileName


    def data(self, fileName):
        global model, SerialNum, fileData, mode, dataDict

        if fileName.lower().endswith('.xml'):
            filepath_class = bioImport()
            fileData = filepath_class.getBioDevData(fileName)
            #print(fileData)
            dataDict = filepath_class.mode() # importing in mode dict from bioimport.py
        elif fileName.lower().endswith('.bnk'):
            bs_class = BscImport()
            #fileData = bs_class.getBscData(fileName)
            #print(fileData)
            dataDict = bs_class.mode(fileName)
            #print(dataDict)
            #dvce_mode = fileData['mode']
            #model = fileData['type']
        elif fileName.lower().endswith('.log'):
            ab_class = AbbotImport()
            #fileData = bs_class.getBscData(fileName)
            #print(fileData)
            dataDict = ab_class.mode(fileName)
        else:
            print('Try Again.')
        return dataDict

if __name__ == "__main__":
    fileName = "BIOIEEE_DDD_CRT.xml"
    #fileName = "02dc396a.bnk"
    #fileName = "abbot.log"
    dataclass = Data()
    datamethod = dataclass.data(fileName)
    #print(datamethod)
    def listData():
        for k, v in iter(datamethod.items()):
            print(k +" : "+ str(v))
    listData()
    #dataclass = bioImport()
    #datamethod = dataclass.getBioDevData(fileName)
    #print(datamethod)
    #print(datamethod)
    #print('mode: ' + datamode['mode'] + ' ' + 'Lower Rate: ' + datamode['lowrate'])
    
