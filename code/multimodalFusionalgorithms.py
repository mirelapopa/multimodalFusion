import numpy as np
import time, datetime
import ast
import downloadFileFromCloud
import uploadFileToCloud
import matplotlib.pyplot as plt
import retrieve_data_ as getDIT
import os
from matplotlib.figure import Figure
from datetime import timedelta
import json
from pprint import pprint
        
class MultimodalFusion():
    
    def __init__(self,mainDiagnose=0,stationaryEvents=[],disease_level=0,dailyMotion=[],nightMotion=[],visitsBathroom=[],abnormalEvents=[],freezing=[],festination=[],lossOfBalance=[],fallDown=[],incontinence=[],leavingHouse=[],digitalTime=[],abnormalDigitalEvents=[],insomnia=0,comorbiditesNeurologist=0,comorbiditesUrinary=0,cognitiveFunctions=0,comorbiditesPsychiatrist=0,depression=0,hipertension=0,comorbiditesCardiovascular=0,medications=[],medicationName=[],evaluationsExercises=[],evaluationsScore=[],evaluationDates=[],evaluationDateList=[],heart_rate_min=[],heart_rate_max=[],heart_rate_mean=[],heart_rate_median=[],heart_rate_mode=[],heart_rate_skewness=[],heart_rate_kurtosis=[],heartRateLow=[],heartRateHigh=[],gsr_min=[],gsr_max=[],gsr_mean=[],gsr_median=[],gsr_mode=[],gsr_skewness=[],gsr_kurtosis=[],steps=[]):
	
		self.mainDiagnose = mainDiagnose
		self.stationaryEvents= stationaryEvents
		self.disease_level = disease_level
		self.dailyMotion = dailyMotion
		self.nightMotion = nightMotion
		self.visitsBathroom = visitsBathroom
		self.abnormalEvents = abnormalEvents
		self.freezing = freezing
		self.festination = festination
		self.lossOfBalance = lossOfBalance
		self.fallDown = fallDown
		self.incontinence = incontinence
		self.leavingHouse = leavingHouse
		self.heartRate_min = heart_rate_min
		self.heartRate_max = heart_rate_max
		self.heartRate_mean = heart_rate_mean
		self.heartRate_median = heart_rate_median
		self.heartRate_mode = heart_rate_mode
		self.heartRate_skewness = heart_rate_skewness
		self.heartRate_kurtosis = heart_rate_kurtosis
		self.heartRateLow = heartRateLow
		self.heartRateHigh = heartRateHigh
		self.steps = steps
		self.galvanicSkinResponse_min = gsr_min
		self.galvanicSkinResponse_max = gsr_max
		self.galvanicSkinResponse_mean = gsr_mean
		self.galvanicSkinResponse_median = gsr_median
		self.galvanicSkinResponse_mode = gsr_mode
		self.galvanicSkinResponse_skewness = gsr_skewness
		self.galvanicSkinResponse_kurtosis = gsr_kurtosis
		self.digitalTime = digitalTime
		self.abnormalDigitalEvents = abnormalDigitalEvents
		self.insomnia = insomnia
		self.depression = depression
		self.hipertension = hipertension
		self.comorbiditesCardiovascular = comorbiditesCardiovascular
		self.comorbiditesNeurologist = comorbiditesNeurologist
		self.comorbiditesUrinary= comorbiditesUrinary
		self.comorbiditesPsychiatrist= comorbiditesPsychiatrist
		self.cognitiveFunctions = cognitiveFunctions
		self.medications = medications
		self.medicationName = medicationName
		self.evaluationsExercises = evaluationsExercises
		self.evaluationsScore = evaluationsScore
		self.evaluationDates = evaluationDates
		self.evaluationDateList = evaluationDateList
		
    def parseHETRAFile(self,filePath,patientId,startDate,nrDays):
	
        stationary = np.zeros(shape =nrDays)
        dailyMotion =  np.zeros(shape =nrDays)
        freezing_events = np.zeros(shape =nrDays)
        festination_events = np.zeros(shape =nrDays)
        loss_of_balance_events = np.zeros(shape =nrDays)
        fall_down_events = np.zeros(shape =nrDays)
        nr_visits_bathroom = np.zeros(shape =nrDays)
        nr_leaving_the_house = np.zeros(shape =nrDays)
        nr_night_visits = np.zeros(shape =nrDays)
        abnormalEvents = np.zeros(shape =nrDays)
        heart_rate_min = np.zeros (shape= (investigatedPeriodinDays))
        heart_rate_max = np.zeros (shape= (investigatedPeriodinDays))
        heart_rate_mean = np.zeros (shape= (investigatedPeriodinDays))
        heart_rate_median = np.zeros (shape= (investigatedPeriodinDays))
        heart_rate_mode = np.zeros (shape= (investigatedPeriodinDays))
        heart_rate_skewness = np.zeros (shape= (investigatedPeriodinDays))
        heart_rate_kurtosis = np.zeros(shape= (investigatedPeriodinDays))
        heartRateLow = np.zeros(shape= (investigatedPeriodinDays))
        heartRateHigh = np.zeros(shape= (investigatedPeriodinDays))
        gsr_min = np.zeros (shape= (investigatedPeriodinDays))
        gsr_max = np.zeros (shape= (investigatedPeriodinDays))
        gsr_mean = np.zeros (shape= (investigatedPeriodinDays))
        gsr_median = np.zeros (shape= (investigatedPeriodinDays))
        gsr_mode = np.zeros (shape= (investigatedPeriodinDays))
        gsr_skewness = np.zeros (shape= (investigatedPeriodinDays))
        gsr_kurtosis = np.zeros (shape= (investigatedPeriodinDays))
        foundPatientId = 0
        indexAnalysis = 0
        startDate = startDate.strftime('%Y-%m-%d')
        startDate =  datetime.datetime.strptime(startDate,'%Y-%m-%d')
        entranceNr_night = 0
        bedroomNr_night = 0
        toiletNr_night = 0
        steps = np.zeros (shape= (investigatedPeriodinDays))
		
        with open(filePath) as f:
            try:
                d = json.load(f)
            except ValueError,e:
				print e
            
            for line in d:
                if ('patientID' in line.keys()):
                    if(line['patientID']==patientId):
                        foundPatientId = 1
                        #print 'found patient'
                        if ('date' in line.keys()):
                            dateFile = datetime.datetime.strptime(str(line['date']),'%Y-%m-%d')
                            difDays = (dateFile-startDate).days
                            indexAnalysis = difDays
                            
                            if ('daily_motion' in line.keys()):
                                daily_dict = line['daily_motion']
                                if (len(daily_dict)!=0):
                                    stationary_ = round(daily_dict.get('stationary',0),2)
                                    fastMov = daily_dict.get('fast_mov',0)
                                    slowMov = daily_dict.get('slow_mov',0)
                                    dailyMov = round(fastMov + slowMov,2)
                                    dailyMotion[indexAnalysis] = dailyMov
                                    stationary[indexAnalysis] = stationary_
                                
                        if('steps' in line.keys()):
                            steps[indexAnalysis] = line['steps']
                                    
                        if('hr' in line.keys()):
                            hr_dict = line['hr']
                            if (len(hr_dict)!=0):
                                heart_rate_min[indexAnalysis] = round(hr_dict.get('min'))
                                heart_rate_max[indexAnalysis] = round(hr_dict.get('max'))
                                heart_rate_mean[indexAnalysis] = round(hr_dict.get('mean'))
                                heart_rate_median[indexAnalysis] = round(hr_dict.get('median'))
                                heart_rate_mode[indexAnalysis] = round(hr_dict.get('mode'))
                                heart_rate_skewness[indexAnalysis] = round(hr_dict.get('skew'))
                                heart_rate_kurtosis[indexAnalysis] = round(hr_dict.get('kurtosis'))
                        if('gsr' in line.keys()):
                            gsr_dict = line['gsr']
                            if (len(gsr_dict)!=0):
                                gsr_min[indexAnalysis] = round(gsr_dict.get('min'))
                                gsr_max[indexAnalysis] = round(gsr_dict.get('max'))
                                gsr_mean[indexAnalysis] = round(gsr_dict.get('mean'))
                                gsr_median[indexAnalysis] = round(gsr_dict.get('median'))
                                gsr_mode[indexAnalysis] = round(gsr_dict.get('mode'))
                                gsr_skewness[indexAnalysis] = round(gsr_dict.get('skew'))
                                gsr_kurtosis[indexAnalysis] = round(gsr_dict.get('kurtosis'))
                        if('heart_rate_low' in line.keys()):
                            hrL_dict = line['heart_rate_low']
                            if (len(hrL_dict)!=0):
                                heartRate_low = round(hrL_dict.get('number'))
                                heartRateLow[indexAnalysis] = heartRate_low
                        if('heart_rate_high' in line.keys()):
                            hrH_dict = line['heart_rate_high']
                            if (len(hrH_dict)!=0):
                                heartRate_high = round(hrH_dict.get('number'))
                                heartRateHigh[indexAnalysis] = heartRate_high
                                
                        if('as_day_motion' in line.keys()):
                            daily_dict = line['as_day_motion']
                            lenDict = len(daily_dict)
                            if(lenDict!=0):
                                toilet_dict = daily_dict.get('toilet')                        
                            
                                toiletNr = len(toilet_dict)
                                if (len(toilet_dict)!=0):
                                    toilet_duration = np.zeros(shape=toiletNr)
                                    for i in range(toiletNr):
                                        toiletItem = toilet_dict[i]
                                        if (len(toiletItem.get('duration'))!=0):
                                            toilet_duration[i] = float(toiletItem.get('duration'))
                                            
                                entrance_dict = daily_dict.get('entrance')
                                entranceNr = len(entrance_dict)
                                if (len(entrance_dict)!=0):
                                    entrance_duration = np.zeros(shape=entranceNr)
                                    for i in range(entranceNr):
                                        entranceItem = entrance_dict[i]
                                        if (len(entranceItem.get('duration'))!=0):
                                            entrance_duration[i] = float(entranceItem.get('duration'))
                                        
                                bedroom_dict = daily_dict.get('bedroom')
                                bedroomNr = len(bedroom_dict)
                                if (len(bedroom_dict)!=0):
                                    bedroom_duration = np.zeros(shape=bedroomNr)
                                    for i in range(bedroomNr):
                                        bedroomItem = bedroom_dict[i]
                                        if (len(bedroomItem.get('duration'))!=0):
                                            bedroom_duration[i] = float(bedroomItem.get('duration'))                                            
                                            
                            if('as_night_motion' in line.keys()):
                                daily_dict = line['as_day_motion']
                                lenDict = len(daily_dict)
                                if(lenDict!=0):
                                    toilet_dict = daily_dict.get('toilet')
                                    toiletNr_night = len(toilet_dict)
                                    if (toiletNr_night!=0):
                                        toiletN_duration = np.zeros(shape=toiletNr_night)
                                        for i in range(toiletNr_night):
                                            eventToilet = toilet_dict[i]
                                            if (len(eventToilet.get('duration'))!=0):
                                                toiletN_duration[i] = float(eventToilet.get('duration'))                                            
                                            
                                    entrance_dict = daily_dict.get('entrance')
                                    entranceNr_night = len(entrance_dict)
                    
                                    if (len(entrance_dict)!=0):
                                        entranceN_duration = np.zeros(shape=entranceNr_night)
                                        for i in range(entranceNr_night):
                                            eventEntrance = entrance_dict[i]
                                            if (len(eventEntrance.get('duration'))!=0):
                                                entranceN_duration[i] = float(eventEntrance.get('duration'))                                            
                                            
                                    bedroom_dict = daily_dict.get('bedroom')
                                    bedroomNr_night = len(bedroom_dict)
                                    if (bedroomNr_night!=0):
                                        bedroomN_duration = np.zeros(shape=bedroomNr_night)
                                        for i in range(bedroomNr_night):
                                            eventBedroom = bedroom_dict[i]
                                            if (len(eventBedroom.get('duration'))!=0):
                                                bedroomN_duration[i] = float(eventBedroom.get('duration'))                                                                                        
                                            
                            nr_night_visits[indexAnalysis] = toiletNr_night + entranceNr_night + bedroomNr_night
                        
                            if('freezing' in line.keys()):
                                freezing_dict = line['freezing']
                                if (len(freezing_dict)!=0):
                                    if('number' in freezing_dict.keys()):
                                        freezing_events[indexAnalysis] = freezing_dict.get('number')
                                        if('event' in freezing_dict.keys()):
                                            freezingEvents = freezing_dict.get('event')
                                            freezingNr = len(freezingEvents)
                                            if(freezingNr>0):
                                                freezing_duration = np.zeros(shape=freezingNr)
                                                for i in range(freezingNr):
                                                    dictfreezing = freezingEvents[i]
                                                    freezing_duration[i] = dictfreezing.get('duration')
                            if('festination' in line.keys()):
                                festination_dict = line['festination']
                                if (len(festination_dict)!=0):
                                    if('number' in festination_dict.keys()):
                                        festination_events[indexAnalysis] = festination_dict.get('number')
                                        if('event' in festination_dict.keys()):
                                            festinationEvents = festination_dict.get('event')
                                            festinationNr = len(festinationEvents)
                                            if(festinationNr>0):
                                                festination_duration = np.zeros(shape=festinationNr)
                                                for i in range(festinationNr):
                                                    dictfestination = festinationEvents[i]
                                                    festination_duration[i] = dictfestination.get('duration')
                            if('loss_of_balance' in line.keys()):
                                loss_of_balance_dict = line['loss_of_balance']
                                if (len(loss_of_balance_dict)!=0):
                                    if('number' in loss_of_balance_dict.keys()):
                                        loss_of_balance_events[indexAnalysis] = loss_of_balance_dict.get('number')
                                        if('event' in loss_of_balance_dict.keys()):
                                            loss_of_balanceEvents = loss_of_balance_dict.get('event')
                                            loss_of_balanceNr = len(loss_of_balanceEvents)
                                            if(loss_of_balanceNr>0):
                                                loss_of_balance_duration = np.zeros(shape=loss_of_balanceNr)
                                                for i in range(loss_of_balanceNr):
                                                    dictloss_of_balance = loss_of_balanceEvents[i]
                                                    loss_of_balance_duration[i] = dictloss_of_balance.get('duration')
                            
                            if('fall_down' in line.keys()):
                                fall_down_dict = line['fall_down']
                                if (len(fall_down_dict)!=0):
                                    if('number' in fall_down_dict.keys()):
                                        fall_down_events[indexAnalysis] = fall_down_dict.get('number')
                                        if('event' in fall_down_dict.keys()):
                                            fall_downEvents = fall_down_dict.get('event')
                                            fall_downNr = len(fall_downEvents)
                                            if(fall_downNr>0):
                                                fall_down_duration = np.zeros(shape=fall_downNr)
                                                for i in range(fall_downNr):
                                                    dictfall_down = fall_downEvents[i]
                                                    fall_down_duration[i] = dictfall_down.get('duration')
                            
                            if('visit_bathroom' in line.keys()):
                                visit_bathroom_dict = line['visit_bathroom']
                                if (len(visit_bathroom_dict)!=0):
                                    if('number' in visit_bathroom_dict.keys()):
                                        nr_visits_bathroom[indexAnalysis] = visit_bathroom_dict.get('number')
                                        if('event' in visit_bathroom_dict.keys()):
                                            visit_bathroomEvents = visit_bathroom_dict.get('event')
                                            visit_bathroomNr = len(visit_bathroomEvents)
                                            if(visit_bathroomNr>0):
                                                visit_bathroom_duration = np.zeros(shape=visit_bathroomNr)
                                                for i in range(visit_bathroomNr):
                                                    dictvisit_bathroom = visit_bathroomEvents[i]
                                                    visit_bathroom_duration[i] = dictvisit_bathroom.get('duration')
                                else:
                                    nr_visits_bathroom[indexAnalysis] = toiletNr + toiletNr_night
                                
                            if('confusion_behavior_detection' in line.keys()):
                                confusion_behavior_detection_dict = line['confusion_behavior_detection']
                                if (len(confusion_behavior_detection_dict)!=0):
                                    if('number' in confusion_behavior_detection_dict.keys()):
                                        abnormalEvents[indexAnalysis] = confusion_behavior_detection_dict.get('number')  
                                        if('event' in confusion_behavior_detection_dict.keys()):
                                            confusion_behavior_detectionEvents = confusion_behavior_detection_dict.get('event')
                                            confusion_behavior_detectionNr = len(confusion_behavior_detectionEvents)
                                            if(confusion_behavior_detectionNr>0):
                                                confusion_behavior_detection_duration = np.zeros(shape=confusion_behavior_detectionNr)
                                                for i in range(confusion_behavior_detectionNr):
                                                    dictconfusion_behavior_detection = confusion_behavior_detectionEvents[i]                            
                                                    confusion_behavior_detection_duration[i] = dictconfusion_behavior_detection.get('duration')
                                            
                            if('leave_the_house' in line.keys()):
                                nrLeavingHouse = line['leave_the_house']
                                if(len(nrLeavingHouse)==0):                            
                                    nr_leaving_the_house[indexAnalysis] = entranceNr + entranceNr_night
                                 
                            if('leave_house_confused' in line.keys()):
                                leavingHouseConfused = line['leave_house_confused']
                        
        return foundPatientId, stationary, dailyMotion, freezing_events, festination_events, loss_of_balance_events, fall_down_events, nr_visits_bathroom, nr_leaving_the_house, nr_night_visits, abnormalEvents, heart_rate_min, heart_rate_max, heart_rate_mean, heart_rate_median, heart_rate_mode, heart_rate_skewness, heart_rate_kurtosis, heartRateLow, heartRateHigh, gsr_min, gsr_max, gsr_mean, gsr_median, gsr_mode, gsr_skewness, gsr_kurtosis, steps    

    def parseEHRFile(self,filePath,patientId,nrDays,startDate,currentDate):

        nrParts = 7
        foundPatientId = 0
        main_diagnosis = -1
        disease_level = 0
        age = 0
        gender = 0
        civilStatus = 0
        bmi =0
        active= 0
        mobility = 0
        depression = 0
        gradeDependence = 0
        autonomousWalk = 0
        independenceDailyActivities = 0
        comorbiditesNeurologist = 0
        comorbiditesPsychiatrist  = 0
        cognitiveFunctions = 0
        comorbiditesCardiovascular = 0
        hipertension = 0
        comorbiditesUrinary = 0
        incontinence = 0
        insomnia = 0
        medicationNames = []
        medications = []
        evaluations = []
        evaluationsScore = []
        evaluationDateList = np.zeros(shape=nrDays)
        evaluationDates = []
        nrMedication = 0

        startDate = datetime.datetime(startDate.year, startDate.month, startDate.day)
        currentDate = datetime.datetime(currentDate.year, currentDate.month, currentDate.day)


        with open(filePath) as f:
            try:
                d = json.load(f)              
                #pprint(d)                    
            except ValueError,e:
                print e
                
            for l in range(len(d)):                   
                line = d[l]
                if ('patientID' in line.keys()):                    
                    if(line['patientID']==patientId):
                        foundPatientId = 1
                        #print patientId
                    else:
                        continue                        
                    
                    if ('mainDiagnosis' in line.keys()):
           
                        if (line['mainDiagnosis']=='Parkinsons'):
                            main_diagnosis = 1
                        elif(line['mainDiagnosis']=='Alzheimers'):
                            main_diagnosis = 0                              
                            #print main_diagnosis
           
                    if ('ParkinsonHoehnAndYard' in line.keys()):           
                        disease_level = int(line['ParkinsonHoehnAndYard'])				
                        
                    if ('MMSE' in line.keys()):
                        mmse = int(line['MMSE'])
                        if(mmse<=10):
                            mmse_score = 5
                        elif(mmse<=19):
                            mmse_score = 4
                        elif(mmse<=24):
                            mmse_score = 3
                        elif(mmse<=27):
                            mmse_score = 2
                        else:
                            mmse_score = 1
                        if(main_diagnosis==0):
                            disease_level = mmse_score
                                
                    if ('dateBirth' in line.keys()):
                        #print line['dateBirth']
                        date_birth = datetime.datetime.strptime(line['dateBirth'],'%Y-%m-%d')
                        currentDay =  datetime.date.today()
                        currentYear = currentDay.year
                        age = currentYear - date_birth.year

                    if ('gender' in line.keys()):  
          
                        gender = int(line['gender'])
           
                    if ('civilStatus' in line.keys()):  
           
                        civil_Status = line['civilStatus']
                        if civil_Status.find('single') > 0:
                            civilStatus = 0
                        elif civil_Status.find('married') > 0:
                            civilStatus = 1
                        elif civil_Status.find('divorced') > 0:
                            civilStatus = 2
                        else:
                            civilStatus = 3                
                            #print civilStatus    
                
                    if ('bmi' in line.keys()):  
                        
                        bmi = int(line['bmi'])           
       
                    if ('active' in line.keys()):             
                        active = int(line['active'])                        
                    if ('mobility' in line.keys()):  
          
                        mobility = int(line['mobility'])
                        
                    if ('depression' in line.keys()):  
          
                        depression = int(line['depression'])
                        
                    if ('gradeDependence' in line.keys()):
                        
                        gradeDependence = int(line['gradeDependence'])

                    if ('autonomousWalk' in line.keys()):
          
                        autonomousWalk = int(line['autonomousWalk'])
                    if ('independenceDailyActivities' in line.keys()):
          
                        independenceDailyActivities = int(line['independenceDailyActivities'])
       
                    if ('comorbiditiesNeurologist' in line.keys()):

                        comorbiditesNeurologist = int(line['comorbiditiesNeurologist'])
           
                    if ('comorbiditiesPsychiatrist' in line.keys()):
          
                        comorbiditesPsychiatrist = int(line['comorbiditiesPsychiatrist'])
                    
                    if ('comorbiditiesCardiovascular' in line.keys()):
          
                        comorbiditesCardiovascular = int(line['comorbiditiesCardiovascular'])
           
                    if ('preserveCognitiveFunctions' in line.keys()):
          
                        cognitiveFunctions = int(line['preserveCognitiveFunctions'])

                    if ('hipertension' in line.keys()):
                        hipertension = int(line['hipertension'])
           
                    if ('comorbiditiesUrinary' in line.keys()):
          
                        comorbiditesUrinary = int(line['comorbiditiesUrinary'])
           
                    if ('incontinence' in line.keys()):
          
                        incontinence = int(line['incontinence'])
       
                    if ('insomnia' in line.keys()):
          
                        insomnia = int(line['insomnia'])
                    
                    if ('SPMSQ' in line.keys()):
                        spmsq = int(line['SPMSQ'])

                    if ('medications' in line.keys()):
                        medication_dict = line['medications']                       
                        nrMedication = len(medication_dict)
                        medications = np.zeros(shape=(nrMedication,nrDays))
                        if(nrMedication>0):
                            for i in range (nrMedication):
                                medicationItem = medication_dict[i]
                                if('history' in medicationItem.keys()):
                                    history_events = medicationItem.get('history')
                                    historyNr = len(history_events)
                                    if (historyNr > 0):
                                        historyItem = history_events[0]
                                        name = historyItem.get('name')
                                        medicationNames.append(name)
                                        for j in range(historyNr):
                                            historyItem = history_events[j]
                                            dosage = historyItem.get('dosage')
                                            active = historyItem.get('active')
                                            dateItem = historyItem.get('date')
                                            ind = dateItem.find('T')
                                            dateItem = datetime.datetime.strptime(dateItem[:ind],'%Y-%m-%d')
                                            if((dateItem>=startDate)&(dateItem<=currentDate)):
                                                indexMed = (dateItem-startDate).days
                                                if(j==0):
                                                    medications[i,indexMed] = 1
                                                else:
                                                    if(dosage!=dosageLastValue):
                                                        medications[i, indexMed] = 2
                                                    elif(active!=activeLastValue):
                                                        medications[i, indexMed] = 3
                                            dosageLastValue = dosage
                                            activeLastValue = active
                        
                    if ('evaluations' in line.keys()):
                        evaluation_dict = line['evaluations']
                        nrEvaluations = len(evaluation_dict)
                        evaluations = np.zeros(shape=(nrEvaluations, nrParts))
                        evaluationsScore = np.zeros(shape=nrEvaluations)
                        if (nrEvaluations > 0):
                            for i in range(nrEvaluations):
                                evaluationItem = evaluation_dict[i]
                                date = evaluationItem.get('date')
                                evaluationDates.append(date)
                                dateItem = datetime.datetime.strptime(date, '%Y-%m-%d')
                                if ((dateItem >= startDate) & (dateItem <= currentDate)):
                                    indexEval = (dateItem - startDate).days
                                    evaluationDateList[indexEval] = i+1
                                score = evaluationItem.get('total')
                                parts = evaluationItem.get('parts')
                                evaluations[i,:]=parts
                                evaluationsScore[i]=score
                        #print evaluations
                        #print evaluationsScore
                        #print evaluationDateList
                    else:
                        str = 'process other functionalities'
                        #print obj                        
                   
        return foundPatientId, main_diagnosis, disease_level, age, gender, civilStatus, bmi, active, mobility, gradeDependence, autonomousWalk, independenceDailyActivities, comorbiditesNeurologist, comorbiditesPsychiatrist, cognitiveFunctions, comorbiditesCardiovascular, hipertension, comorbiditesUrinary, incontinence, insomnia, depression, medications, medicationNames, evaluations, evaluationsScore, evaluationDates, evaluationDateList
    
    def parseDITFile_allEvents(self,filePath,nrDays,startDay):
        
        totalTimeUsageperDayInterval = np.zeros(shape= 3*nrDays)
        totalTimeUsageperDay = np.zeros(shape= nrDays)
        
        with open(filePath,'r') as inf:
            for line in inf:
                functionalityName = line
                
                if(functionalityName.find("eventTime")>0):
                    fieldName = functionalityName.split(':')[1]
                    obj = fieldName.split('"')[1]
                    obj_ = obj.split('/')
                    obj_day = obj_[1]
                    currentday = int(obj_day)-startDay+1
                                       
                    obj_time = obj_[2].split(' ')[1]
                    currentTime = int(obj_time)
                    
                    if(currentTime<12):
                        currentTimeIndex = 0
                    elif(currentTime<18):
                        currentTimeIndex = 1
                    else:
                        currentTimeIndex = 2
                    currentIndex = (currentday-1)*3 + currentTimeIndex
                    
                    totalTimeUsageperDayInterval[currentIndex] = totalTimeUsageperDayInterval[currentIndex] + 1
                    totalTimeUsageperDay[currentday-1] = totalTimeUsageperDay[currentday-1] + 1                           
                    
        return totalTimeUsageperDay

    def parseDITFile_ABD(self,filePath,nrDays,startDay):
    
        abnormalUsageTime = np.zeros(shape= nrDays)
        nrAbnormalEvents = np.zeros(shape= nrDays)
        type_events_T = np.zeros(shape= nrDays)
        type_events_S = np.zeros(shape= nrDays)
        type_events_ST = np.zeros(shape= nrDays)
        nr_newAttachment = np.zeros(shape= nrDays)
        nr_kBase = np.zeros(shape= nrDays)
        nr_medication = np.zeros(shape= nrDays) 
    
        with open(filePath,'r') as inf:
        
            for line in inf:          
          
                functionalityName = line
                if functionalityName.find("eventTime") > 0 :       
               
                    fieldName = functionalityName.split(':')[1]
                    obj = fieldName.split('"')[1]
                    obj_date = obj.split(' ')[0]                  
                    index_day = int(obj_date.split('/')[1])    
                    index_day = index_day - startDay+1
                             
                elif functionalityName.find("doctype") > 0 :
           
                    fieldName = functionalityName.split(':')[1]
                    obj = fieldName.split(',')[0]
                    nrAbnormalEvents[index_day-1] = nrAbnormalEvents[index_day-1] + 1
           
                    if obj.find("ST") > 0:
                        type_events_ST[index_day-1] = type_events_ST[index_day-1] + 1 
                    elif obj.find("S") > 0:
                        type_events_S[index_day-1] = type_events_S[index_day-1] + 1 
                    elif obj.find("T") > 0:
                        type_events_T[index_day-1] = type_events_T[index_day-1] + 1     
           
                elif functionalityName.find("elapsedTime") > 0:
           
                    fieldName = functionalityName.split(':')[1]
                    obj = fieldName.split(',')[0]
           
                    abnormalUsageTime[index_day-1] = abnormalUsageTime[index_day-1] + int(obj)
                    #print abnormalUsageTime
           
                elif functionalityName.find("function") > 0:
           
                    fieldName = functionalityName.split(':')[1]
                    obj = fieldName.split(',')[0]           
                    if obj.find("NEW_ATTACHMENT") > 0:
                        nr_newAttachment[index_day-1] = nr_newAttachment[index_day-1] + 1 
                    elif obj.find("K_BASE") > 0:
                        nr_kBase[index_day-1] = nr_kBase[index_day-1] + 1                            
                    elif obj.find("FORM_MEDICACION") > 0:                
                        nr_medication[index_day-1] = nr_medication[index_day-1] + 1                               
                  
        #print abnormalUsageTime, nrAbnormalEvents, type_events_T, type_events_S, type_events_ST, nrFunctionCalls_newAttachment, nrFunctionCalls_kBase, nrFunctionCalls_medication 
        return abnormalUsageTime, nrAbnormalEvents, type_events_T, type_events_S, type_events_ST         
       
    def evaluateParkinsonsActivities(self,outputFile,investigatedPeriodinDays):
        
        halfInterval = int(investigatedPeriodinDays/2) 
        
        #evaluation of stationary behaviour
        stationary = self.stationaryEvents       
        maxValue = max(stationary)
        
        if maxValue>0:
            stationary_ = stationary/maxValue
        else:
            stationary_ = stationary
               
        stationary_period1 = np.mean(stationary_[:halfInterval])
        stationary_period2 = np.mean(stationary_[halfInterval:])
        
        percent_stationary = stationary_period2 -stationary_period1
        
        if percent_stationary > 0.1:
            line = 'Apathy increase of: ' + str(round(percent_stationary*100,2)) + '%; ' + str(stationary) + "\n"        
        elif percent_stationary < -0.1:
            line = 'Activity increase, stationary behaviour decrease of: ' + str(round(-percent_stationary*100,2)) + '%; ' + str(stationary) +  "\n"            
        else:
            line = "Apathy: no signs; "  + str(stationary) +  "\n"                                 
        print line
        
        line = '\t\t\"stationaryBehaviour\":{\n' + '\t\t\t\"result\":' + str(round(percent_stationary*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,stationary))+'\n\t\t\t]\n' + '\t\t},\n'
                
        outputFile.writelines(line)
        
        if(percent_stationary>=0):
            probabilityApathy_stationary = 0.5*percent_stationary
            probabilityImprovedBehaviour_stationary = 0.001
        else:
            # for a decreasing stationary behaviour the probability of apathy is very low
            probabilityApathy_stationary = 0.001
            probabilityImprovedBehaviour_stationary = -0.3*percent_stationary
        
        #plot a graph of the stationary behaviour over the investigated days
        showGraph_apathy = 0
        if showGraph_apathy:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(stationary)),int(max(stationary))]
            plt.plot(stationary,'ro')
            plt.axis(days_axis)
            plt.xlabel('Amount of stationary behaviour over the investigated days')
            plt.show()    
   
        #assess the steps received from the band
        steps = self.steps
        maxValue = max(steps)
        if maxValue>0:
            steps_ = steps/maxValue
        else:
            steps_ = steps
            
        steps_period1 = np.mean(steps_[:halfInterval])
        steps_period2 = np.mean(steps_[halfInterval:])
    
        percent_steps = steps_period2 - steps_period1        
        if percent_steps > 0.1:
            line = 'General daily motion (based on steps) increase of: ' + str(round(percent_steps*100)) + '%; ' + str(steps) + "\n"           
        elif percent_steps < -0.1:
            line = 'General daily motion (based on steps) decrease of: ' + str(round(-percent_steps*100)) + '%; ' + str(steps) +  "\n"            
        else:
            line = "General daily motion (based on steps) no deviations; "  + str(steps) +  "\n"           
        print line
                
        line = '\t\t\"overallMotion\":{\n' + '\t\t\t\"result\":' + str(round(percent_steps*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,steps))+'\n\t\t\t]\n' + '\t\t},\n'
        outputFile.writelines(line)
        
        #in the case daily motion calculated using the nr of steps decreases, the probability of apathy increases
        if(percent_steps<0):
            probabilityApathy_steps = -percent_steps*0.2
            probabilityImprovedBehaviour_steps = 0.001
        else:
            # for increasing daily motion the probability of apathy is very low
            probabilityApathy_steps = 0.001
            probabilityImprovedBehaviour_steps= 0.2*percent_steps
        
        #assess the daily motion
        dailyMotion = self.dailyMotion
        maxValue = max(dailyMotion)
        if maxValue>0:
            dailyMotion_ = dailyMotion/maxValue
        else:
            dailyMotion_ = dailyMotion
            
        dailyMotion_period1 = np.mean(dailyMotion_[:halfInterval])
        dailyMotion_period2 = np.mean(dailyMotion_[halfInterval:])
    
        percent_dailyMotion = dailyMotion_period2 -dailyMotion_period1        
        if percent_dailyMotion > 0.1:
            line = 'Daily motion increase of: ' + str(round(percent_dailyMotion*100)) + '%; ' + str(dailyMotion) + "\n"           
        elif percent_dailyMotion < -0.1:
            line = 'Daily motion decrease of: ' + str(round(-percent_dailyMotion*100)) + '%; ' + str(dailyMotion) +  "\n"            
        else:
            line = "Daily motion no deviations; "  + str(dailyMotion) +  "\n"           
        print line
                
        line = '\t\t\"dailyMotion\":{\n' + '\t\t\t\"result\":' + str(round(percent_dailyMotion*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,dailyMotion))+'\n\t\t\t]\n' + '\t\t},\n'
        outputFile.writelines(line)
        
        #in the case daily motion decreases, the probability of apathy increases
        if(percent_dailyMotion<0):
            probabilityApathy_dailyMotion = -percent_dailyMotion*0.15
            probabilityImprovedBehaviour_dailyMotion = 0.001
        else:
            # for increasing daily motion the probability of apathy is very low
            probabilityApathy_dailyMotion = 0.001
            probabilityImprovedBehaviour_dailyMotion= 0.15*percent_dailyMotion
                
        #plot a graph of the daily motion behaviour over the investigated days
        showGraph_dailyMotion = 0
        if showGraph_dailyMotion:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(dailyMotion)),int(max(dailyMotion))]
            plt.plot(dailyMotion,'ro')
            plt.axis(days_axis)
            plt.xlabel('Amount of daily motion over the investigated days')
            plt.show()
        
        # evaluation of the number of leaving the house events
        nr_leaving_the_house = self.leavingHouse
        maxValue = max(nr_leaving_the_house)
        if maxValue>0:
            nr_leaving_the_house_ = nr_leaving_the_house/maxValue
        else:
            nr_leaving_the_house_ = nr_leaving_the_house
                
        leavingHouse_period1 = np.mean(nr_leaving_the_house_[:halfInterval])    
        leavingHouse_period2 = np.mean(nr_leaving_the_house_[halfInterval:])
        
        percent_leavingHouse = leavingHouse_period2 - leavingHouse_period1 
                    
        if percent_leavingHouse > 0.1:
            line = 'Patient leaving the house, increase of: ' + str(round(percent_leavingHouse*100)) + '%; ' + str(nr_leaving_the_house) + "\n"
            
        elif percent_leavingHouse < -0.1:
            line = 'Patient leaving the house, decrease of: ' + str(round(-percent_leavingHouse*100)) + '%; ' + str(nr_leaving_the_house) + "\n"
            
        else:
            line = 'Patient leaving the house, no deviations; ' + str(nr_leaving_the_house) + "\n"
        print line
        
        if(percent_leavingHouse<0):
            probabilityApathy_leavingHouse = -0.3*percent_leavingHouse
            probabilityImprovedBehaviour_leavingHouse = 0.001
        else:
            # for decreasing leaving of the house events the probability of apathy is very low
            probabilityApathy_leavingHouse = 0.001
            probabilityImprovedBehaviour_leavingHouse = 0.3*percent_leavingHouse
    
        line = '\t\t\"leavingHouse\":{\n' + '\t\t\t\"result\":' + str(round(percent_leavingHouse*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,nr_leaving_the_house))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
       
        #plot a graph of the leaving the house over the investigated days
        showGraph_leaving = 0
        if showGraph_leaving:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(nr_leaving_the_house)),int(max(nr_leaving_the_house))]
            plt.plot(nr_leaving_the_house,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of leaving the house events over the investigated days')
            plt.show()
    
        #evaluation of the number of visits during the night
        nr_night_visits = self.nightMotion
        maxValue = max(nr_night_visits)
        if maxValue>0:
            nr_night_visits_ = nr_night_visits/maxValue
        else:
            nr_night_visits_ = nr_night_visits
            
        # assess deviations in the night motion
        nightMotion_period1 = np.mean(nr_night_visits_[:halfInterval])    
        nightMotion_period2 = np.mean(nr_night_visits_[halfInterval:])
        
        percent_nightMotion = nightMotion_period2-nightMotion_period1 
                
        if percent_nightMotion > 0.1:
            line = 'Night motion, increase of: ' + str(round(percent_nightMotion*100)) + '%; ' + str(nr_night_visits) + "\n"
            probabilityInsomnia_nightMotion = percent_nightMotion
            
        elif percent_nightMotion < -0.1:
            line = 'Night motion, decrease of: ' + str(round(-percent_nightMotion*100)) + '%; ' + str(nr_night_visits) + "\n"
            
        else:
            line = 'Night motion, no deviations; ' + str(nr_night_visits) + "\n"                 
        print line
        
        line = '\t\t\"nightMotion\":{\n' + '\t\t\t\"result\":' + str(round(percent_nightMotion*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,nr_night_visits))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
    
        insomnia = self.insomnia
        line = '\t\t\"insomnia\":'+str(insomnia)+',\n'
        outputFile.writelines(line)
    
        if(percent_nightMotion>=0):
            probabilityInsomnia_nightMotion = percent_nightMotion
            probabilityImprovedBehaviour_nightMotion = 0.001            
        else:
            # for decreasing night motion the probability of insomnia is very low
            probabilityInsomnia_nightMotion = 0.001
            probabilityImprovedBehaviour_nightMotion = -0.2*percent_nightMotion
                      
        if(insomnia):
            probabilityInsomnia_nightMotion = 0.4*probabilityInsomnia_nightMotion                        
        else:
            probabilityInsomnia_nightMotion = 0.6*probabilityInsomnia_nightMotion            
                
        #plot a graph of the night motion over the investigated days
        showGraph_nightMotion = 0
        if showGraph_nightMotion:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(nr_night_visits)),int(max(nr_night_visits))]
            plt.plot(nr_night_visits,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of events during the night over the investigated days')
            plt.show()
        
        #assess the freezing events for detecting deviations 
        freezing_events = self.freezing
        maxValue = max(freezing_events)
        if maxValue>0:
            freezing_events_ = freezing_events/maxValue
        else:
            freezing_events_ = freezing_events
            
        freezing_period1 = np.mean(freezing_events_[:halfInterval])
        freezing_period2 = np.mean(freezing_events_[halfInterval:])
        
        percent_freezing = freezing_period2 - freezing_period1
       
        if percent_freezing > 0.1:
        
            line = 'Freezing events, increase of: ' + str(round(percent_freezing*100))+ '%; ' + str(freezing_events) + "\n"
                    
        elif percent_freezing < -0.1:
            line = 'Freezing events, decrease of: ' + str(round(-percent_freezing*100)) + '%; ' + str(freezing_events) + "\n"
            
        else:
            line = 'Freezing events, no deviations; ' + str(freezing_events) + "\n"
        print line
                
        line = '\t\t\"freezing\":{\n' + '\t\t\t\"result\":' + str(round(percent_freezing*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,freezing_events))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
        
        if(percent_freezing>=0):            
            probabilityParkinsonsEvents_freezing = 0.3*percent_freezing
            probabilityImprovedBehaviour_freezing = 0.001
        else:
            # for decreasing freezing events the probability of Parkinson events is very low
            probabilityParkinsonsEvents_freezing = 0.001 
            probabilityImprovedBehaviour_freezing = -0.2*percent_freezing
            
        #plot a graph of the freezing events over the investigated days
        showGraph_freezing = 0
        if showGraph_freezing:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(freezing_events)),int(max(freezing_events))]
            plt.plot(freezing_events,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of freezing events over the investigated days')
            plt.show()
        
        #assess the festination events for detecting deviations 
        festination_events = self.festination
        maxValue = max(festination_events)
        if maxValue>0:
            festination_events_ = festination_events/maxValue
        else:
            festination_events_ = festination_events
            
        festination_period1 = np.mean(festination_events_[:halfInterval])
        festination_period2 = np.mean(festination_events_[halfInterval:])
        
        percent_festination = festination_period2 - festination_period1
        
        if percent_festination > 0.5:        
            line = 'Festination events, increase of: ' + str(round(percent_festination*100))+ '%; ' + str(festination_events) + "\n"
            line1 = 'Therefore, a visit to the neurologist would be indicated.'
                    
        elif percent_festination > 0.1:                
            line = 'Festination events, increase of: '  + str(round(percent_festination*100))+ '%; ' + str(festination_events) + "\n"
                    
        elif percent_festination < -0.1:
            line = 'Festination events, decrease of: ' + str(round(-percent_festination*100))+ '%; ' + str(festination_events) + "\n"            
        else:
            line = 'Festination events, no deviations; ' + str(festination_events) + "\n"
        print line
                
        line = '\t\t\"festination\":{\n' + '\t\t\t\"result\":' + str(round(percent_festination*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,festination_events))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
    
        if(percent_festination>=0):            
            probabilityParkinsonsEvents_festination = 0.3*percent_festination
            probabilityImprovedBehaviour_festination = 0.001
        else:
            # for decreasing festination events the probability of Parkinson events is very low
            probabilityParkinsonsEvents_festination = 0.001 
            probabilityImprovedBehaviour_festination = -0.2*percent_festination
            
        #check if there is a correlation between the freezing and festination events
        if (percent_festination > 0.1)&(percent_freezing > 0.1):
            line = 'Increase in both festination and freezing events of: '  + str(round(percent_festination*100))+ '% and ' + str(round(percent_freezing*100))+ '%; ' + "\n"
            print line         
        elif (percent_festination < 0)&(percent_freezing < 0):
            line = 'Decrease in both festination and freezing events of: '  + str(round(percent_festination*100))+ '% and ' + str(round(percent_freezing*100))+ '%; ' + "\n"
            print line         
    
        # check if medication was prescribed in the evaluated period   
    
        #plot a graph of the festination events over the investigated days
        showGraph_festination = 0
        if showGraph_festination:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(festination_events)),int(max(festination_events))]
            plt.plot(festination_events,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of festination events over the investigated days')
            plt.show()
        
        #assess the  fall down event  deviations
        fall_down_events = self.fallDown
        maxValue = max(fall_down_events)
        if maxValue>0:
            fall_down_events_ = fall_down_events/maxValue
        else:
            fall_down_events_ = fall_down_events
            
        fall_down_period1 = np.mean(fall_down_events_[:halfInterval])
        fall_down_period2 = np.mean(fall_down_events_[halfInterval:])
        
        percent_fall_down = fall_down_period2 - fall_down_period1 
        
        if percent_fall_down > 0.3:
        
            line = 'Fall down events, increase of: ' + str(round(percent_fall_down*100))+ '%; ' + str(fall_down_events) + "\n"
            line1 = 'Therefore, a visit to the neurologist would be indicated.'
                   
        elif percent_fall_down > 0.1:
                
            line = 'Fall down events, increase of: ' + str(round(percent_fall_down*100))+ '%; ' + str(fall_down_events) + "\n"
            
        elif percent_fall_down < -0.1:
            line = 'Fall down events, decrease of: ' + str(round(-percent_fall_down*100))+ '%; ' + str(fall_down_events) + "\n"
            
        else:
            line = 'Fall down events, no deviations; '+ str(fall_down_events) + "\n"
        print line
                
        line = '\t\t\"fallDown\":{\n' + '\t\t\t\"result\":' + str(round(percent_fall_down*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,fall_down_events))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
        
        if(percent_fall_down>=0):            
            probabilityParkinsonsEvents_fall_down = 0.2*percent_fall_down
            probabilityImprovedBehaviour_fallDown = 0.001
        else:
            # for decreasing falling down events the probability of Parkinson events is very low
            probabilityParkinsonsEvents_fall_down = 0.001 
            probabilityImprovedBehaviour_fallDown = -0.2*percent_fall_down
            
        #plot a graph of the falling down events over the investigated days
        showGraph_fall = 0
        if showGraph_fall:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(fall_down_events)),int(max(fall_down_events))]
            plt.plot(fall_down_events,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of falling down events over the investigated days')
            plt.show()
        
        #assess the loss of balance event deviations 
        loss_of_balance_events = self.lossOfBalance
        maxValue = max(loss_of_balance_events)
        if maxValue>0:
            loss_of_balance_events_ = loss_of_balance_events/maxValue
        else:
            loss_of_balance_events_ = loss_of_balance_events

        loss_of_balance_period1 = np.mean(loss_of_balance_events_[:halfInterval])
        loss_of_balance_period2 = np.mean(loss_of_balance_events_[halfInterval:])
              
        percent_loss_of_balance = loss_of_balance_period2 - loss_of_balance_period1
        
        if percent_loss_of_balance > 0.5 :
            line = 'Loss of balance events, increase of: ' + str(round(percent_loss_of_balance*100))+ '%; ' + str(loss_of_balance_events) + "\n"
            line1 = 'Therefore, a visit to the neurologist would be indicated.'
        
        elif percent_loss_of_balance > 0.1:
                
            line = 'Loss of balance events, increase of: '  + str(round(percent_loss_of_balance*100))+ '%; ' + str(loss_of_balance_events) + "\n"
        
        elif percent_loss_of_balance < -0.1:
            line = 'Loss of balance events, decrease of: ' + str(round(-percent_loss_of_balance*100))+ '%; ' + str(loss_of_balance_events) + "\n"
        
        else:
            line = 'Loss of balance events, no deviations; '+ str(loss_of_balance_events) + "\n"
        print line
        
    
        line = '\t\t\"lossBalance\":{\n' + '\t\t\t\"result\":' + str(round(percent_loss_of_balance*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,loss_of_balance_events))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
    
        #plot a graph of the loss of balance events over the investigated days
        showGraph_lossBalance = 0
        if showGraph_lossBalance:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(loss_of_balance_events)),int(max(loss_of_balance_events))]
            plt.plot(loss_of_balance_events,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of loss of balance events over the investigated days')
            plt.show()

        if(percent_loss_of_balance>=0):            
            probabilityParkinsonsEvents_lossBalance = 0.2*percent_loss_of_balance
            probabilityImprovedBehaviour_lossBalance = 0.001
        else:
            # for decreasing loss of balance events the probability of Parkinson events is very low
            probabilityParkinsonsEvents_lossBalance = 0.001 
            probabilityImprovedBehaviour_lossBalance = -0.2*percent_loss_of_balance

        #assess the deviations in the number of visits to the bathroom
        nr_visits_bathroom = self.visitsBathroom
        maxValue = max(nr_visits_bathroom)
        if maxValue>0:
            nr_visits_bathroom_ = nr_visits_bathroom/maxValue
        else:
            nr_visits_bathroom_ = nr_visits_bathroom
            
        nr_visits_bathroom_period1 = np.mean(nr_visits_bathroom_[:halfInterval])
        nr_visits_bathroom_period2 = np.mean(nr_visits_bathroom_[halfInterval:])
        
        percent_nr_visits_bathroom = nr_visits_bathroom_period2 - nr_visits_bathroom_period1 
        
        if percent_nr_visits_bathroom > 0.3:
        
            line = 'Number of visits to the bathroom, increase of: ' + str(round(percent_nr_visits_bathroom*100))+ '%; ' + str(nr_visits_bathroom) + "\n"
                   
            if (self.comorbiditesUrinary > 0) or (self.incontinence > 0):
                line1 = 'As the patient has also some urinary problems, a visit to the professional is indicated.'              
                   
        elif percent_nr_visits_bathroom > 0.1:
                
            line = 'Number of visits to the bathroom, increase of: ' + str(round(percent_nr_visits_bathroom*100))+ '%; ' + str(nr_visits_bathroom) + "\n"
                   
        elif percent_nr_visits_bathroom < -0.1:
            line = 'Number of visits to the bathroom, decrease of: ' + str(round(-percent_nr_visits_bathroom*100))+ '%; ' + str(nr_visits_bathroom) + "\n"
           
        else:
            line = 'Number of visits to the bathroom, no deviations; '  + str(nr_visits_bathroom) + "\n"
        print line
            
        line = '\t\t\"visitBathroom\":{\n' + '\t\t\t\"result\":' + str(round(percent_nr_visits_bathroom*100)) + ',\n' +'\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,nr_visits_bathroom))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
        
        incontinence = self.incontinence
        
        line = '\t\t\"incontinence\":'+str(incontinence) + ', \n'
        outputFile.writelines(line)

        if(percent_nr_visits_bathroom>=0):            
            probabilityIncontinence_visitsBathroom = 0.7*(percent_nr_visits_bathroom)
        else:
            # for decreasing number of visits to the bathroom the probability of Parkinson events is very low
            probabilityIncontinence_visitsBathroom = 0.001 
        probabilityIncontinence_medicalCondition = 0.3*incontinence 
        incontinenceProb = probabilityIncontinence_medicalCondition  + probabilityIncontinence_visitsBathroom                        
        
        #plot a graph of the number of visits to the bathroom over the investigated days
        showGraph_bathroom = 0
        if showGraph_bathroom:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(nr_visits_bathroom)),int(max(nr_visits_bathroom))]
            plt.plot(nr_visits_bathroom,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of visits to the bathroom over the investigated days')
            plt.show()
                
        #assess the heart rate events for detecting deviations 
        hr_events = self.heartRate_mean
        hr_events_min = self.heartRate_min
        hr_events_max = self.heartRate_max
        hr_events_median = self.heartRate_median
        hr_events_mode = self.heartRate_mode
        hr_events_skewness = self.heartRate_skewness
        hr_events_kurtosis = self.heartRate_kurtosis
        maxValue = max(hr_events)
        if maxValue>0:
            hr_events_ = hr_events/maxValue
        else:
            hr_events_ = hr_events
            
        hr_period1 = np.mean(hr_events_[:halfInterval])
        hr_period2 = np.mean(hr_events_[halfInterval:])
        
        percent_hr = hr_period2 - hr_period1
       
        if percent_hr > 0.2:
        
            line = 'Heart rate, increase of: ' + str(round(percent_hr*100))+ '%; ' + str(hr_events) + "\n"
                    
        elif percent_hr < -0.2:
            line = 'Heart rate, decrease of: ' + str(round(-percent_hr*100)) + '%; ' + str(hr_events) + "\n"
            
        else:
            line = 'Heart rate, no significant deviations; ' + str(hr_events) + "\n"
        print line                
        
        line = '\t\t\"heart_rate\":{\n' 
        outputFile.writelines(line)
        line='\t\t\t\"result\":' + str(round(percent_hr*100)) + ',\n' 
        line = line + '\t\t\t\"meanHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events))+'\n\t\t\t],\n' 
        line = line + '\t\t\t\"minHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events_min))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"maxHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events_max))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"medianHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events_median))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"modeHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events_mode))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"skewnessHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events_skewness))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"kurtosisHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events_kurtosis))+'\n\t\t\t],\n'                                             
        line = line + '\t\t},\n'              
        outputFile.writelines(line)
        
        if(abs(percent_hr)>=0.2):            
            probabilityHipertension_hr= 0.7*(percent_hr)
        else:
            probabilityHipertension_hr = 0.001
        probabilityHipertension_medicalCondition = 0.3*self.hipertension
        hipertensionProb = probabilityHipertension_medicalCondition  + probabilityHipertension_hr                        
        
        if(abs(percent_hr)>=0.2):            
            probabilityCardiovascular_hr= 0.7*(percent_hr)
        else:
            probabilityCardiovascular_hr = 0.001
        probabilityCardiovascular_medicalCondition = 0.3*self.comorbiditesCardiovascular
        cardiovascularProb = probabilityCardiovascular_medicalCondition  + probabilityCardiovascular_hr
        
         #assess the heart rate events for detecting deviations 
        gsr_events = self.galvanicSkinResponse_mean
        gsr_min = self.galvanicSkinResponse_min
        gsr_max = self.galvanicSkinResponse_max
        gsr_median = self.galvanicSkinResponse_median
        gsr_mode = self.galvanicSkinResponse_mode
        gsr_skewness = self.galvanicSkinResponse_skewness
        gsr_kurtosis = self.galvanicSkinResponse_kurtosis
        
        maxValue = max(gsr_events)
        if maxValue>0:
            gsr_events_ = gsr_events/maxValue
        else:
            gsr_events_ = gsr_events
            
        gsr_period1 = np.mean(gsr_events_[:halfInterval])
        gsr_period2 = np.mean(gsr_events_[halfInterval:])
        
        percent_gsr = gsr_period2 - gsr_period1
       
        if percent_gsr > 0.2:
        
            line = 'Galvanic skin response, increase of: ' + str(round(percent_gsr*100))+ '%; ' + str(gsr_events) + "\n"
                    
        elif percent_gsr < -0.2:
            line = 'Galvanic skin response, decrease of: ' + str(round(-percent_gsr*100)) + '%; ' + str(gsr_events) + "\n"
            
        else:
            line = 'Galvanic skin response, no significant deviations; ' + str(gsr_events) + "\n"
        print line                     
        
        line = '\t\t\"galvanic skin response\":{\n' 
        outputFile.writelines(line)
        line='\t\t\t\"result\":' + str(round(percent_gsr*100)) + ',\n' 
        line = line + '\t\t\t\"meanGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_events))+'\n\t\t\t],\n' 
        line = line + '\t\t\t\"minGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_min))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"maxGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_max))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"medianGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_median))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"modeGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_mode))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"skewnessGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_skewness))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"kurtosisGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_kurtosis))+'\n\t\t\t],\n'                                             
        line = line + '\t\t},\n'              
        outputFile.writelines(line)
        
        #assess the deviations in the time spent on digital devices
        time_dit = self.digitalTime
        maxValue = max(time_dit)        
        if maxValue>0:
            time_dit_ = time_dit/maxValue
        else:
            time_dit_ = time_dit

        time_dit1 = np.mean(time_dit_[:halfInterval])
        time_dit2 = np.mean(time_dit_[halfInterval:])
      
        percent_time_dit = time_dit2 - time_dit1 
        
        if percent_time_dit > 0.3:
        
            line = 'Time spent on digital devices, increase of: ' + str(round(percent_time_dit*100))+ '%; ' + str(time_dit) + "\n"
            print line         
            #outputFile.writelines(line)        
        
        elif percent_time_dit > 0.1:
                
            line = 'Time spent on digital devices, increase of: ' + str(round(percent_time_dit*100))+ '%; ' + str(time_dit) + "\n" 
                    
        elif percent_time_dit < -0.1:
            line = 'Time spent on digital devices, decrease of: ' + str(round(-percent_time_dit*100))+ '%; ' + str(time_dit) + "\n" 
            
        else:
            line = 'Time spent on digital devices, no deviations; '+ str(time_dit) + "\n" 
        print line
                
        line = '\t\t\"digitalTimeSpent\":{\n' + '\t\t\t\"result\":' + str(round(percent_time_dit*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,time_dit))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
        
        if(percent_time_dit>=0):            
            probabilityDigitalAddiction_timeDit = 0.6*(percent_time_dit)
            probabilityApathy_timeDit = 0.2*(percent_time_dit)            
        else:
            # for decreasing digital time usage the probability of addiction is very low
            probabilityDigitalAddiction_timeDit = 0.001 
            probabilityApathy_timeDit = 0.001

        probabilityDigitalAddiction_depression =  0.3*self.depression
        probDigitalAddiction = probabilityDigitalAddiction_depression + probabilityDigitalAddiction_timeDit
               
        #plot a graph of the time spent on dit over the investigated days
        showGraph_time = 0
        if showGraph_time:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(time_dit)),int(max(time_dit))]
            plt.plot(time_dit,'ro')
            plt.axis(days_axis)
            plt.xlabel('Amount of time spent on the digital platform over the investigated days')
            plt.show()

        #assess deviations in the number of dit abnormal behaviours
        nr_abnormal_dit_behaviours = self.abnormalDigitalEvents
        maxValue = max(nr_abnormal_dit_behaviours)
        if maxValue>0:
            nr_abnormal_dit_behaviours_ = nr_abnormal_dit_behaviours/maxValue
        else:
            nr_abnormal_dit_behaviours_ = nr_abnormal_dit_behaviours

        abnormal_dit1 = np.mean(nr_abnormal_dit_behaviours_[:halfInterval])
        abnormal_dit2 = np.mean(nr_abnormal_dit_behaviours_[halfInterval:])

        percent_abnormal_dit = abnormal_dit2 - abnormal_dit1 
        
        if percent_abnormal_dit > 0.3:
        
            line = 'Number of abnormal digital behaviours, increase of: '+ str(round(percent_abnormal_dit*100))+ '%; ' + str(nr_abnormal_dit_behaviours) + "\n" 
            
            if (self.comorbiditesNeurologist > 0):
                line1 = 'A visit would be indicated to the professional in charge of the patient, due to an increase in the digital abnormal behaviour. \n'
                print line1
                            
        elif percent_abnormal_dit > 0.1:
                
            line = 'Number of abnormal digital behaviours, increase of: ' + str(round(percent_abnormal_dit*100))+ '%; ' + str(nr_abnormal_dit_behaviours) + "\n" 
                    
        elif percent_abnormal_dit < -0.1:
            line = 'Number of abnormal digital behaviours, decrease of: ' + str(round(-percent_abnormal_dit*100))+ '%; ' + str(nr_abnormal_dit_behaviours) + "\n" 
            
        else:
            line = 'Number of abnormal digital behaviours, no deviations; '  + str(nr_abnormal_dit_behaviours) + "\n" 
        print line
             
        line = '\t\t\"abnormalDigitalBehaviours\":{\n' + '\t\t\t\"result\":' + str(round(percent_abnormal_dit*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,nr_abnormal_dit_behaviours))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)

        if(percent_abnormal_dit>=0):            
            probabilityDigitalConfusion_abnormalDigitalBehaviour = percent_abnormal_dit
            probabilityImprovedBehaviour_abnormalDigitalBehaviour = 0.001
        else:
            # for decreasing number of abnormal digital events the probability of digital confusion is very low
            probabilityDigitalConfusion_abnormalDigitalBehaviour = 0.001 
            probabilityImprovedBehaviour_abnormalDigitalBehaviour = -0.2*percent_abnormal_dit

        #plot a graph of the digital abnormal behaviours over the investigated days
        showGraph_abnormal = 0
        if showGraph_abnormal:
			#fig = plt.figure()
			days_axis = [1,investigatedPeriodinDays,int(min(nr_abnormal_dit_behaviours)),int(max(nr_abnormal_dit_behaviours))]
			plt.plot(nr_abnormal_dit_behaviours,'ro')
			plt.axis(days_axis)
			plt.xlabel('Number of digital abnormal behaviours events over the investigated days')
			plt.show()
		
        # assess medication changes
        nrMedications=len(self.medicationName)        
        changes = np.zeros(shape=nrMedications)       
        indexMedication = np.zeros(shape=nrMedications)
        line = '\t\t\"medication\":[\n'
      
        for i in range(nrMedications):            
            line = line + '\t\t{\n' +'\t\t\t\"name\":' + self.medicationName[i] +',\n'
            line = line + '\t\t\t\"changes\":' + '['+', '.join(map(str,self.medications[i,:]))+']' +'\n'
            
            changes[i] =np.sum(self.medications[i,:])
            if(changes[i]>0):
                indexMedication[i] = 1
            if(i==nrMedications-1):
                line= line + '\t\t}\n'
            else:	
                line = line + '\t\t},\n'
        line = line + '\t\t],\n'
        outputFile.writelines(line)
        changeMedication = np.sum(changes)

        #check if in the analyzed period there was a change in any of the medications
        if(changeMedication>0):
            # compute the probability based on the number of changed medications
            # in this version only Parkinsons medication is considered, and this is changed only one at a certain moment
            # either by changing the ddosage, prescribing a new one or stopping a current one
            probabilityImprovedBehaviour_medicationChange = 0.2*np.sum(indexMedication)
            probabilityParkinsonsEvents_medicationChange = 0.2 * np.sum(indexMedication)
        else:
            probabilityImprovedBehaviour_medicationChange = 0.01
            probabilityParkinsonsEvents_medicationChange = 0.01

        # assess movement evaluation
        nrEvaluations = len(self.evaluationDates)
        line = '\t\t\"movementEvaluations\":[\n'
        for i in range(nrEvaluations):
            line = line + '\t\t{\n' + '\t\t\t\"date\":' + self.evaluationDates[i] + ',\n'
            line = line + '\t\t\t\"totalScore\":' + str(self.evaluationsScore[i]) + ',\n'
            line = line + '\t\t\t\"partScores\":' + '[' + ', '.join(map(str, self.evaluationsExercises[i, :])) + ']' + '\n'
            line = line + '\t\t},\n'

        outputFile.writelines(line)

        # check if there are movement evaluations in the analyzed period
        nrParts = self.evaluationsExercises.shape[1]
        percentageParts = np.zeros(nrParts)
        percentageEvaluation = 0

        if(np.sum(self.evaluationDateList)>0):
            #check if there at least 2 evaluations
            if(nrEvaluations>1):
                if(self.evaluationsScore[nrEvaluations-1]+self.evaluationsScore[nrEvaluations-2]>0):
                    percentageEvaluation = (self.evaluationsScore[nrEvaluations-1]-self.evaluationsScore[nrEvaluations-2])/(self.evaluationsScore[nrEvaluations-1]+self.evaluationsScore[nrEvaluations-2])
                else:
                    percentageEvaluation = 0

                for i in range(nrParts):
                    if(self.evaluationsExercises[nrEvaluations - 1,i] + self.evaluationsExercises[nrEvaluations - 2,i]>0):
                        percentageParts[i] = (self.evaluationsExercises[nrEvaluations - 1,i] - self.evaluationsExercises[nrEvaluations - 2,i]) / (self.evaluationsExercises[nrEvaluations - 1,i] + self.evaluationsExercises[nrEvaluations - 2,i])
                    else:
                        percentageParts[i] = 0
                percentageParts = np.round(percentageParts,2)

        line = '\t\t{\n' + '\t\t\t\"totalScoreDeviation\":' + str(round(percentageEvaluation,3)) + ',\n'
        line = line + '\t\t\t\"partsDeviation\":' + '[' + ', '.join(map(str, percentageParts)) + ']' + '\n' + '\t\t}\n'
        line = line + '\t\t],\n'
        outputFile.writelines(line)

        if (percentageEvaluation >= 0):
            probabilityImprovedBehaviour_movementEvolution = 0.2 * percentageEvaluation
        else:
            probabilityImprovedBehaviour_movementEvolution = 0.01

        cognitiveFunctions = self.cognitiveFunctions
        if(cognitiveFunctions):
            probabilityDigitalConfusion_abnormalDigitalBehaviour = 0.6*probabilityDigitalConfusion_abnormalDigitalBehaviour		
            probDigitalConfusion = probabilityDigitalConfusion_abnormalDigitalBehaviour
        else:
            probabilityDigitalConfusion_abnormalDigitalBehaviour = 0.7*probabilityDigitalConfusion_abnormalDigitalBehaviour		
            probDigitalConfusion =probabilityDigitalConfusion_abnormalDigitalBehaviour + 0.3*(1-int(cognitiveFunctions))
        
        probabilityInsomnia_digitalAddiction = 0.2*probDigitalAddiction
        probabilityInsomnia_depression = 0.2*self.depression
        probabilityInsomnia_medicalCondition = 0.3*insomnia
        insomniaProb = probabilityInsomnia_medicalCondition + probabilityInsomnia_nightMotion + probabilityInsomnia_depression + probabilityInsomnia_digitalAddiction

        if(insomniaProb>1):
            insomniaProb = 0.9
            
        line = '\t\t\"probabilities\":[\n' 
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Insomnia|nightMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityInsomnia_nightMotion,3)) + '\n\t\t},\n'
        outputFile.writelines(line)  
        
        line = '\t\t{\n\t\t\t\"type\":\"Insomnia|digitalAddiction\",\n'+'\t\t\t\"value\":'+str(round(probabilityInsomnia_digitalAddiction,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Insomnia|depression\",\n'+'\t\t\t\"value\":'+str(round(probabilityInsomnia_depression,3)) + '\n\t\t},\n'
        outputFile.writelines(line)   
        
        line = '\t\t{\n\t\t\t\"type\":\"Insomnia|medicalCondition\",\n'+'\t\t\t\"value\":'+str(round(probabilityInsomnia_medicalCondition,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"sleepDisorders\",\n'+'\t\t\t\"value\":'+str(round(insomniaProb,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Incontinence|visitsBathroom\",\n'+'\t\t\t\"value\":'+str(round(probabilityIncontinence_visitsBathroom,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Incontinence|medicalCondition\",\n'+'\t\t\t\"value\":'+str(round( probabilityIncontinence_medicalCondition,3)) + '\n\t\t},\n'
        outputFile.writelines(line)          
        
        line = '\t\t{\n\t\t\t\"type\":\"Incontinence\",\n'+'\t\t\t\"value\":'+str(round(incontinenceProb,3)) + '\n\t\t},\n'
        outputFile.writelines(line)              
             
        line = '\t\t{\n\t\t\t\"type\":\"Hipertension|biologicalMeasurements\",\n'+'\t\t\t\"value\":'+str(round(probabilityHipertension_hr,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Hipertension|medicalCondition\",\n'+'\t\t\t\"value\":'+str(round( probabilityHipertension_medicalCondition,3)) + '\n\t\t},\n'
        outputFile.writelines(line)  

        line = '\t\t{\n\t\t\t\"type\":\"Hipertension\",\n'+'\t\t\t\"value\":'+str(round(hipertensionProb,3)) + '\n\t\t},\n'
        outputFile.writelines(line)              
        
        line = '\t\t{\n\t\t\t\"type\":\"Cardiovascular condition|biologicalMeasurements\",\n'+'\t\t\t\"value\":'+str(round(probabilityCardiovascular_hr,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Cardiovascular condition|medicalCondition\",\n'+'\t\t\t\"value\":'+str(round(probabilityCardiovascular_medicalCondition,3)) + '\n\t\t},\n'
        outputFile.writelines(line)  

        line = '\t\t{\n\t\t\t\"type\":\"Cardiovascular condition\",\n'+'\t\t\t\"value\":'+str(round(cardiovascularProb,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"digitalAddiction|digitalTimeUsage\",\n'+'\t\t\t\"value\":'+str(round(probabilityDigitalAddiction_timeDit,3)) + '\n\t\t},\n'
        outputFile.writelines(line)            
        
        line = '\t\t{\n\t\t\t\"type\":\"digitalAddiction|depression\",\n'+'\t\t\t\"value\":'+str(round(probabilityDigitalAddiction_depression,3)) + '\n\t\t},\n'
        outputFile.writelines(line)            
                
        line = '\t\t{\n\t\t\t\"type\":\"digitalAddiction\",\n'+'\t\t\t\"value\":'+str(round(probDigitalAddiction,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"digitalConfusion|abnormalDigitalBehaviour\",\n'+'\t\t\t\"value\":'+str(round(probabilityDigitalConfusion_abnormalDigitalBehaviour,3)) + '\n\t\t},\n'
        outputFile.writelines(line)   
        
        line = '\t\t{\n\t\t\t\"type\":\"digitalConfusion\",\n'+'\t\t\t\"value\":'+str(round(probDigitalConfusion,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        probApathy = probabilityApathy_stationary + probabilityApathy_dailyMotion + probabilityApathy_leavingHouse + probabilityApathy_timeDit + probabilityApathy_steps
        if(probApathy>1):
            probApathy = 1
                  
        line = '\t\t{\n\t\t\t\"type\":\"Apathy|stationaryBehaviour\",\n'+'\t\t\t\"value\":'+str(round(probabilityApathy_stationary,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Apathy|dailyMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityApathy_dailyMotion,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Apathy|overallMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityApathy_steps,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Apathy|leavingHouse\",\n'+'\t\t\t\"value\":'+str(round(probabilityApathy_leavingHouse,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Apathy|digitalTimeUsage\",\n'+'\t\t\t\"value\":'+str(round(probabilityApathy_timeDit,3)) + '\n\t\t},\n'
        outputFile.writelines(line)

        line = '\t\t{\n\t\t\t\"type\":\"Apathy\",\n'+'\t\t\t\"value\":'+str(round(probApathy,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        probParkinsonsEvents = probabilityParkinsonsEvents_festination + probabilityParkinsonsEvents_freezing + probabilityParkinsonsEvents_fall_down  + probabilityParkinsonsEvents_lossBalance
        
        line = '\t\t{\n\t\t\t\"type\":\"ParkinsonsEvents|freezing\",\n'+'\t\t\t\"value\":'+str(round(probabilityParkinsonsEvents_freezing,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ParkinsonsEvents|festination\",\n'+'\t\t\t\"value\":'+str(round(probabilityParkinsonsEvents_festination,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ParkinsonsEvents|fallDown\",\n'+'\t\t\t\"value\":'+str(round(probabilityParkinsonsEvents_fall_down,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ParkinsonsEvents|lossOfBalance\",\n'+'\t\t\t\"value\":'+str(round(probabilityParkinsonsEvents_lossBalance,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)

        # adjust the probability based on the p(ParkinsonsEvents)
        if(probParkinsonsEvents<0.1):
            probabilityParkinsonsEvents_medicationChange = 0.01
        line = '\t\t{\n\t\t\t\"type\":\"ParkinsonsEvents|medicationChange\",\n' + '\t\t\t\"value\":' + str(round(probabilityParkinsonsEvents_medicationChange, 3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        #line = '\t\t{\n\t\t\t\"type\":\"ParkinsonsEvents|movementEvaluation\",\n' + '\t\t\t\"value\":' + str(round(probabilityParkinsonsEvents_movementEvaluation, 3)) + '\n\t\t},\n'
        #outputFile.writelines(line)

        line = '\t\t{\n\t\t\t\"type\":\"ParkinsonsEvents\",\n'+'\t\t\t\"value\":'+str(round(probParkinsonsEvents,3)) + '\n\t\t},\n'
        outputFile.writelines(line)

        probImprovedBehaviour = probabilityImprovedBehaviour_abnormalDigitalBehaviour + probabilityImprovedBehaviour_dailyMotion + probabilityImprovedBehaviour_fallDown + probabilityImprovedBehaviour_festination + probabilityImprovedBehaviour_freezing + probabilityImprovedBehaviour_lossBalance + probabilityImprovedBehaviour_nightMotion + probabilityImprovedBehaviour_stationary + probabilityImprovedBehaviour_leavingHouse + probabilityImprovedBehaviour_movementEvolution + probabilityImprovedBehaviour_steps
        
        if(probImprovedBehaviour>1):
            probImprovedBehaviour = 1       
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|stationary\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_stationary,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|dailyMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_dailyMotion,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|overallMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_steps,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|nightMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_nightMotion,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|leavingHouse\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_leavingHouse,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|fallDown\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_fallDown,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|festination\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_festination,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|freezing\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_freezing,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|lossOfBalance\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_lossBalance,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)

        #line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|movementEvaluation\",\n' + '\t\t\t\"value\":' + str(round(probabilityImprovedBehaviour_movementEvaluation, 3)) + '\n\t\t},\n'
        #outputFile.writelines(line)

        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|abnormalDigitalBehaviour\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_abnormalDigitalBehaviour,3)) + '\n\t\t},\n'
        outputFile.writelines(line)

        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|movementEvolution\",\n' + '\t\t\t\"value\":' + str(
            round(probabilityImprovedBehaviour_movementEvolution, 3)) + '\n\t\t},\n'
        outputFile.writelines(line)

        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour\",\n'+'\t\t\t\"value\":'+str(round(probImprovedBehaviour,3)) + '\n\t\t}\n'                                    
        outputFile.writelines(line)

        if(probImprovedBehaviour < 0.1):
            probabilityImprovedBehaviour_medicationChange = 0.01
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|medicationChange\",\n' + '\t\t\t\"value\":' + str(
            round(probabilityImprovedBehaviour_medicationChange, 3)) + '\n\t\t},\n'
        outputFile.writelines(line)


        line = '\t\t]\n'
        outputFile.writelines(line)    
       
    def evaluateAlzheimersActivities(self,outputFile,investigatedPeriodinDays):    
        
        halfInterval = int(investigatedPeriodinDays/2) 
        
        #evaluation of stationary behaviour
        stationary = self.stationaryEvents
        maxValue = max(stationary)
        if maxValue>0:
            stationary_ = stationary/maxValue
        else:
            stationary_ = stationary
               
        stationary_period1 = np.mean(stationary_[:halfInterval])
        stationary_period2 = np.mean(stationary_[halfInterval:])
        
        percent_stationary = stationary_period2 -stationary_period1
        
        if percent_stationary > 0.1:
            line = 'Apathy increase of: ' + str(round(percent_stationary*100,2)) + '%; ' + str(stationary) + "\n"        
        elif percent_stationary < -0.1:
            line = 'Activity increase, stationary behaviour decrease of: ' + str(round(-percent_stationary*100,2)) + '%; ' + str(stationary) +  "\n"            
        else:
            line = "Apathy: no signs; "  + str(stationary) +  "\n"                                 
        print line
        
        line = '\t\t\"stationaryBehaviour\":{\n' + '\t\t\t\"result\":' + str(round(percent_stationary*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,stationary))+'\n\t\t\t]\n' + '\t\t},\n'
        outputFile.writelines(line)
        
        if(percent_stationary>=0):
            probabilityApathy_stationary = 0.5*percent_stationary
            probabilityImprovedBehaviour_stationary = 0.001
            probabilityMovementIssues_stationary = 0.3*percent_stationary
        else:
            # for a decreasing stationary behaviour the probability of apathy is very low
            probabilityApathy_stationary = 0.001
            probabilityImprovedBehaviour_stationary = -0.3*percent_stationary
            probabilityMovementIssues_stationary = 0.001
        
        #plot a graph of the stationary behaviour over the investigated days
        showGraph_apathy = 0
        if showGraph_apathy:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(stationary)),int(max(stationary))]
            plt.plot(stationary,'ro')
            plt.axis(days_axis)
            plt.xlabel('Amount of stationary behaviour over the investigated days')
            plt.show()    
        
         #assess the steps received from the band
        steps = self.steps
        maxValue = max(steps)
        if maxValue>0:
            steps_ = steps/maxValue
        else:
            steps_ = steps
            
        steps_period1 = np.mean(steps_[:halfInterval])
        steps_period2 = np.mean(steps_[halfInterval:])
    
        percent_steps = steps_period2 - steps_period1        
        if percent_steps > 0.1:
            line = 'General daily motion (based on steps) increase of: ' + str(round(percent_steps*100)) + '%; ' + str(steps) + "\n"           
        elif percent_steps < -0.1:
            line = 'General daily motion (based on steps) decrease of: ' + str(round(-percent_steps*100)) + '%; ' + str(steps) +  "\n"            
        else:
            line = "General daily motion (based on steps) no deviations; "  + str(steps) +  "\n"           
        print line
                
        line = '\t\t\"overallMotion\":{\n' + '\t\t\t\"result\":' + str(round(percent_steps*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,steps))+'\n\t\t\t]\n' + '\t\t},\n'
        outputFile.writelines(line)
        
        #in the case daily motion calculated using the nr of steps decreases, the probability of apathy increases
        if(percent_steps<0):
            probabilityApathy_steps = -percent_steps*0.2
            probabilityImprovedBehaviour_steps = 0.001
            probabilityMovementIssues_steps =-0.2*percent_steps
        else:
            # for increasing daily motion the probability of apathy is very low
            probabilityApathy_steps = 0.001
            probabilityMovementIssues_steps = 0.001
            probabilityImprovedBehaviour_steps= 0.2*percent_steps
            
        #assess the daily motion
        dailyMotion = self.dailyMotion
        maxValue = max(dailyMotion)
        if maxValue>0:
            dailyMotion_ = dailyMotion/maxValue
        else:
            dailyMotion_ = dailyMotion
            
        dailyMotion_period1 = np.mean(dailyMotion_[:halfInterval])
        dailyMotion_period2 = np.mean(dailyMotion_[halfInterval:])
    
        percent_dailyMotion = dailyMotion_period2 -dailyMotion_period1        
        if percent_dailyMotion > 0.1:
            line = 'Daily motion increase of: ' + str(round(percent_dailyMotion*100)) + '%; ' + str(dailyMotion) + "\n"           
        elif percent_dailyMotion < -0.1:
            line = 'Daily motion decrease of: ' + str(round(-percent_dailyMotion*100)) + '%; ' + str(dailyMotion) +  "\n"            
        else:
            line = "Daily motion no deviations; "  + str(dailyMotion) +  "\n"           
        print line
                
        line = '\t\t\"dailyMotion\":{\n' + '\t\t\t\"result\":' + str(round(percent_dailyMotion*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,dailyMotion))+'\n\t\t\t]\n' + '\t\t},\n'
        outputFile.writelines(line)
        
        #in the case daily motion decreases, the probability of apathy increases
        if(percent_dailyMotion<0):
            probabilityApathy_dailyMotion = -percent_dailyMotion*0.3
            probabilityImprovedBehaviour_dailyMotion = 0.001
            probabilityMovementIssues_dailyMotion =-0.2*percent_dailyMotion
        else:
            # for increasing daily motion the probability of apathy is very low
            probabilityApathy_dailyMotion = 0.001
            probabilityImprovedBehaviour_dailyMotion= 0.3*percent_dailyMotion
            probabilityMovementIssues_dailyMotion = 0.001
            
            
        #plot a graph of the daily motion behaviour over the investigated days
        showGraph_dailyMotion = 0
        if showGraph_dailyMotion:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(dailyMotion)),int(max(dailyMotion))]
            plt.plot(dailyMotion,'ro')
            plt.axis(days_axis)
            plt.xlabel('Amount of daily motion over the investigated days')
            plt.show()
        
        # evaluation of the number of leaving the house events
        nr_leaving_the_house = self.leavingHouse
        maxValue = max(nr_leaving_the_house)
        if maxValue>0:
            nr_leaving_the_house_ = nr_leaving_the_house/maxValue
        else:
            nr_leaving_the_house_ = nr_leaving_the_house
                
        leavingHouse_period1 = np.mean(nr_leaving_the_house_[:halfInterval])    
        leavingHouse_period2 = np.mean(nr_leaving_the_house_[halfInterval:])
        
        percent_leavingHouse = leavingHouse_period2 - leavingHouse_period1 
                    
        if percent_leavingHouse > 0.1:
            line = 'Leaving the house events, increase of: ' + str(round(percent_leavingHouse*100)) + '%; ' + str(nr_leaving_the_house) + "\n"
            
        elif percent_leavingHouse < -0.1:
            line = 'Leaving the house events, decrease of: ' + str(round(-percent_leavingHouse*100)) + '%; ' + str(nr_leaving_the_house) + "\n"
            
        else:
            line = 'Leaving the house events, no deviations; ' + str(nr_leaving_the_house) + "\n"
        print line
        
        if(percent_leavingHouse<0):
            probabilityApathy_leavingHouse = -0.3*percent_leavingHouse
            probabilityImprovedBehaviour_leavingHouse = 0.001
            probabilityMovementIssues_leavingHouse = -0.2*percent_leavingHouse
        else:
            # for decreasing leaving of the house events the probability of apathy is very low
            probabilityApathy_leavingHouse = 0.001
            probabilityImprovedBehaviour_leavingHouse = 0.3*percent_leavingHouse
            probabilityMovementIssues_leavingHouse = 0.001
    
        line = '\t\t\"leavingHouse\":{\n' + '\t\t\t\"result\":' + str(round(percent_leavingHouse*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,nr_leaving_the_house))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
                   
        #assess the heart rate events for detecting deviations 
        hr_events = self.heartRate_mean
        hr_events_min = self.heartRate_min
        hr_events_max = self.heartRate_max
        hr_events_median = self.heartRate_median
        hr_events_mode = self.heartRate_mode
        hr_events_skewness = self.heartRate_skewness
        hr_events_kurtosis = self.heartRate_kurtosis
        maxValue = max(hr_events)
        if maxValue>0:
            hr_events_ = hr_events/maxValue
        else:
            hr_events_ = hr_events
            
        hr_period1 = np.mean(hr_events_[:halfInterval])
        hr_period2 = np.mean(hr_events_[halfInterval:])
        
        percent_hr = hr_period2 - hr_period1
       
        if percent_hr > 0.2:
        
            line = 'Heart rate, increase of: ' + str(round(percent_hr*100))+ '%; ' + str(hr_events) + "\n"
                    
        elif percent_hr < -0.2:
            line = 'Heart rate, decrease of: ' + str(round(-percent_hr*100)) + '%; ' + str(hr_events) + "\n"
            
        else:
            line = 'Heart rate, no significant deviations; ' + str(hr_events) + "\n"
        print line                
        
        line = '\t\t\"heart_rate\":{\n' 
        outputFile.writelines(line)
        line='\t\t\t\"result\":' + str(round(percent_hr*100)) + ',\n' 
        line = line + '\t\t\t\"meanHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events))+'\n\t\t\t],\n' 
        line = line + '\t\t\t\"minHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events_min))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"maxHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events_max))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"medianHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events_median))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"modeHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events_mode))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"skewnessHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events_skewness))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"kurtosisHeartRate\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events_kurtosis))+'\n\t\t\t],\n'                                             
        line = line + '\t\t},\n'              
        outputFile.writelines(line)
        
        if(abs(percent_hr)>=0.2):            
            probabilityHipertension_hr= 0.7*(percent_hr)
        else:
            probabilityHipertension_hr = 0.001
        probabilityHipertension_medicalCondition = 0.3*self.hipertension
        hipertensionProb = probabilityHipertension_medicalCondition  + probabilityHipertension_hr                        
        
        if(abs(percent_hr)>=0.2):            
            probabilityCardiovascular_hr= 0.7*(percent_hr)
        else:
            probabilityCardiovascular_hr = 0.001
        probabilityCardiovascular_medicalCondition = 0.3*self.comorbiditesCardiovascular
        cardiovascularProb = probabilityCardiovascular_medicalCondition  + probabilityCardiovascular_hr
        
         #assess the heart rate events for detecting deviations 
        gsr_events = self.galvanicSkinResponse_mean
        gsr_min = self.galvanicSkinResponse_min
        gsr_max = self.galvanicSkinResponse_max
        gsr_median = self.galvanicSkinResponse_median
        gsr_mode = self.galvanicSkinResponse_mode
        gsr_skewness = self.galvanicSkinResponse_skewness
        gsr_kurtosis = self.galvanicSkinResponse_kurtosis
        
        maxValue = max(gsr_events)
        if maxValue>0:
            gsr_events_ = gsr_events/maxValue
        else:
            gsr_events_ = gsr_events
            
        gsr_period1 = np.mean(gsr_events_[:halfInterval])
        gsr_period2 = np.mean(gsr_events_[halfInterval:])
        
        percent_gsr = gsr_period2 - gsr_period1
       
        if percent_gsr > 0.2:
        
            line = 'Galvanic skin response, increase of: ' + str(round(percent_gsr*100))+ '%; ' + str(gsr_events) + "\n"
                    
        elif percent_gsr < -0.2:
            line = 'Galvanic skin response, decrease of: ' + str(round(-percent_gsr*100)) + '%; ' + str(gsr_events) + "\n"
            
        else:
            line = 'Galvanic skin response, no significant deviations; ' + str(gsr_events) + "\n"
        print line                     
        
        line = '\t\t\"galvanic skin response\":{\n' 
        outputFile.writelines(line)
        line='\t\t\t\"result\":' + str(round(percent_gsr*100)) + ',\n' 
        line = line + '\t\t\t\"meanGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_events))+'\n\t\t\t],\n' 
        line = line + '\t\t\t\"minGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_min))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"maxGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_max))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"medianGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_median))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"modeGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_mode))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"skewnessGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_skewness))+'\n\t\t\t],\n'
        line = line + '\t\t\t\"kurtosisGSR\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,gsr_kurtosis))+'\n\t\t\t],\n'                                             
        line = line + '\t\t},\n'              
        outputFile.writelines(line)     
                       
        #plot a graph of the leaving the house over the investigated days
        showGraph_leaving = 0
        if showGraph_leaving:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(nr_leaving_the_house)),int(max(nr_leaving_the_house))]
            plt.plot(nr_leaving_the_house,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of leaving the house events over the investigated days')
            plt.show()
    
        #evaluation of the number of visits during the night
        nr_night_visits = self.nightMotion
        maxValue = max(nr_night_visits)
        if maxValue>0:
            nr_night_visits_ = nr_night_visits/maxValue
        else:
            nr_night_visits_ = nr_night_visits
            
        # assess deviations in the night motion
        nightMotion_period1 = np.mean(nr_night_visits_[:halfInterval])    
        nightMotion_period2 = np.mean(nr_night_visits_[halfInterval:])
        
        percent_nightMotion = nightMotion_period2-nightMotion_period1 
                
        if percent_nightMotion > 0.1:
            line = 'Night motion, increase of: ' + str(round(percent_nightMotion*100)) + '%; ' + str(nr_night_visits) + "\n"
            probabilityInsomnia_nightMotion = percent_nightMotion
            
        elif percent_nightMotion < -0.1:
            line = 'Night motion, decrease of: ' + str(round(-percent_nightMotion*100)) + '%; ' + str(nr_night_visits) + "\n"
            
        else:
            line = 'Night motion, no deviations; ' + str(nr_night_visits) + "\n"                 
        print line
        
        line = '\t\t\"nightMotion\":{\n' + '\t\t\t\"result\":' + str(round(percent_nightMotion*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,nr_night_visits))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
    
        insomnia = self.insomnia
        line = '\t\t\"insomnia\":'+str(insomnia)+',\n'
        outputFile.writelines(line)
    
        if(percent_nightMotion>=0):
            probabilityInsomnia_nightMotion = percent_nightMotion
            probabilityImprovedBehaviour_nightMotion = 0.001            
        else:
            # for decreasing night motion the probability of insomnia is very low
            probabilityInsomnia_nightMotion = 0.001
            probabilityImprovedBehaviour_nightMotion = -0.2*percent_nightMotion
                      
        if(insomnia):
            probabilityInsomnia_nightMotion = 0.4*probabilityInsomnia_nightMotion           
            
        else:
            probabilityInsomnia_nightMotion = 0.6*probabilityInsomnia_nightMotion            
      
        #plot a graph of the night motion over the investigated days
        showGraph_nightMotion = 0
        if showGraph_nightMotion:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(nr_night_visits)),int(max(nr_night_visits))]
            plt.plot(nr_night_visits,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of events during the night over the investigated days')
            plt.show()
        
        #assess the abnormal behaviours
        abnormalEvents = self.abnormalEvents
        maxValue = max(abnormalEvents)
        if maxValue>0:
            abnormalEvents_ = abnormalEvents/maxValue
        else:
            abnormalEvents_ = abnormalEvents
            
        abnormalEvents_period1 = np.mean(abnormalEvents_[:halfInterval])
        abnormalEvents_period2 = np.mean(abnormalEvents_[halfInterval:])
    
        percent_abnormalEvents = abnormalEvents_period2 -abnormalEvents_period1        
        
        if(percent_abnormalEvents>0.1):
            line = 'Abnormal events increase of: ' + str(round(percent_abnormalEvents*100)) + '%; ' + str(abnormalEvents) + '\n'
        elif(percent_abnormalEvents<-0.1):
            line = 'Abnormal events decrease of: ' + str(round(-percent_abnormalEvents*100)) + '%; ' + str(abnormalEvents) +  '\n'
        else:                   
            line = "Abnormal events no deviations; "  + str(abnormalEvents) +  "\n"
        print line
                
        line = '\t\t\"abnormalEvents\":{\n' + '\t\t\t\"result\":' + str(round(percent_abnormalEvents*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,abnormalEvents))+'\n\t\t\t]\n' + '\t\t},\n' 
        outputFile.writelines(line)
        
        if(percent_abnormalEvents>=0):
            probabilityConfusion_abnormalEvents = percent_abnormalEvents
            probabilityImprovedBehaviour_abnormalEvents = 0.001  
        else:
            # for decreasing confused events, the probability of confusion is very low
            probabilityConfusion_abnormalEvents = 0.001
            probabilityImprovedBehaviour_abnormalEvents = -0.2*percent_abnormalEvents
         
        comorbiditesNeurologist= self.comorbiditesNeurologist 
        comorbiditesPsychiatrist = self.comorbiditesPsychiatrist
       
        probabilityComorbiditesNeurologist = comorbiditesNeurologist
        probabilityComorbiditesPsychiatrist = comorbiditesPsychiatrist            
            
        if(comorbiditesPsychiatrist&comorbiditesNeurologist):
            probabilityConfusion_abnormalEvents = 0.5*probabilityConfusion_abnormalEvents
            probabilityComorbiditesNeurologist = 0.25*comorbiditesNeurologist
            probabilityComorbiditesPsychiatrist = 0.25*comorbiditesPsychiatrist            
        elif(comorbiditesPsychiatrist):
            probabilityConfusion_abnormalEvents = 0.65*probabilityConfusion_abnormalEvents
            probabilityComorbiditesPsychiatrist = 0.4*comorbiditesPsychiatrist                        
        elif(comorbiditesNeurologist):
            probabilityConfusion_abnormalEvents = 0.65*probabilityConfusion_abnormalEvents
            probabilityComorbiditesNeurologist = 0.3*comorbiditesNeurologist            
        else:
            probabilityConfusion_abnormalEvents = 0.7*probabilityConfusion_abnormalEvents            
            
        probConfusion = probabilityConfusion_abnormalEvents + probabilityComorbiditesNeurologist + probabilityComorbiditesPsychiatrist
                         
        #plot a graph of the confused behaviour over the investigated days
        showGraph_abnormalEvents = 0
        if showGraph_abnormalEvents:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(abnormalEvents)),int(max(abnormalEvents))]
            plt.plot(abnormalEvents,'ro')
            plt.axis(days_axis)
            plt.xlabel('Amount of abnormal events over the investigated days')
            plt.show()            
               
        # check if medication was prescribed in the evaluated period   
            
        #assess the  fall down event  deviations
        fall_down_events = self.fallDown
        maxValue = max(fall_down_events)
        if maxValue>0:
            fall_down_events_ = fall_down_events/maxValue
        else:
            fall_down_events_ = fall_down_events
            
        fall_down_period1 = np.mean(fall_down_events_[:halfInterval])
        fall_down_period2 = np.mean(fall_down_events_[halfInterval:])
        
        percent_fall_down = fall_down_period2 - fall_down_period1 
        
        if percent_fall_down > 0.3:
        
            line = 'Fall down events, increase of: ' + str(round(percent_fall_down*100))+ '%; ' + str(fall_down_events) + "\n"
            line1 = 'Therefore, a visit to the neurologist would be indicated.'
                   
        elif percent_fall_down > 0.1:
                
            line = 'Fall down events, increase of: ' + str(round(percent_fall_down*100))+ '%; ' + str(fall_down_events) + "\n"
            
        elif percent_fall_down < -0.1:
            line = 'Fall down events, decrease of: ' + str(round(-percent_fall_down*100))+ '%; ' + str(fall_down_events) + "\n"
            
        else:
            line = 'Fall down events, no deviations; '+ str(fall_down_events) + "\n"
        print line
                
        line = '\t\t\"fallDown\":{\n' + '\t\t\t\"result\":' + str(round(percent_fall_down*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,fall_down_events))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
        
        if(percent_fall_down>=0):            
            probabilityMovementIssues_fall_down = 0.3*percent_fall_down
            probabilityImprovedBehaviour_fallDown = 0.001
        else:
            # for decreasing falling down events the probability of Parkinson events is very low
            probabilityMovementIssues_fall_down = 0.01 
            probabilityImprovedBehaviour_fallDown = -0.2*percent_fall_down
            
        #plot a graph of the falling down events over the investigated days
        showGraph_fall = 0
        if showGraph_fall:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(fall_down_events)),int(max(fall_down_events))]
            plt.plot(fall_down_events,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of falling down events over the investigated days')
            plt.show()
        
        #assess the loss of balance event deviations 
        loss_of_balance_events = self.lossOfBalance
        maxValue = max(loss_of_balance_events)
        if maxValue>0:
            loss_of_balance_events_ = loss_of_balance_events/maxValue
        else:
            loss_of_balance_events_ = loss_of_balance_events

        loss_of_balance_period1 = np.mean(loss_of_balance_events_[:halfInterval])
        loss_of_balance_period2 = np.mean(loss_of_balance_events_[halfInterval:])
              
        percent_loss_of_balance = loss_of_balance_period2 - loss_of_balance_period1
        
        if percent_loss_of_balance > 0.5 :
            line = 'Loss of balance events, increase of: ' + str(round(percent_loss_of_balance*100))+ '%; ' + str(loss_of_balance_events) + "\n"
            line1 = 'Therefore, a visit to the neurologist would be indicated.'
        
        elif percent_loss_of_balance > 0.1:
                
            line = 'Loss of balance events, increase of: '  + str(round(percent_loss_of_balance*100))+ '%; ' + str(loss_of_balance_events) + "\n"
        
        elif percent_loss_of_balance < -0.1:
            line = 'Loss of balance events, decrease of: ' + str(round(-percent_loss_of_balance*100))+ '%; ' + str(loss_of_balance_events) + "\n"
        
        else:
            line = 'Loss of balance events, no deviations; '+ str(loss_of_balance_events) + "\n"
        print line       
    
        line = '\t\t\"lossBalance\":{\n' + '\t\t\t\"result\":' + str(round(percent_loss_of_balance*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,loss_of_balance_events))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
    
        #plot a graph of the loss of balance events over the investigated days
        showGraph_lossBalance = 0
        if showGraph_lossBalance:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(loss_of_balance_events)),int(max(loss_of_balance_events))]
            plt.plot(loss_of_balance_events,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of loss of balance events over the investigated days')
            plt.show()

        if(percent_loss_of_balance>=0):            
            probabilityMovementIssues_lossBalance = 0.2*percent_loss_of_balance
            probabilityImprovedBehaviour_lossBalance = 0.001
        else:
            # for decreasing loss of balance events the probability of Parkinson events is very low
            probabilityMovementIssues_lossBalance = 0.01 
            probabilityImprovedBehaviour_lossBalance = -0.2*percent_loss_of_balance

        #assess the deviations in the number of visits to the bathroom
        nr_visits_bathroom = self.visitsBathroom
        maxValue = max(nr_visits_bathroom)
        if maxValue>0:
            nr_visits_bathroom_ = nr_visits_bathroom/maxValue
        else:
            nr_visits_bathroom_ = nr_visits_bathroom
            
        nr_visits_bathroom_period1 = np.mean(nr_visits_bathroom_[:halfInterval])
        nr_visits_bathroom_period2 = np.mean(nr_visits_bathroom_[halfInterval:])
        
        percent_nr_visits_bathroom = nr_visits_bathroom_period2 - nr_visits_bathroom_period1 
        
        if percent_nr_visits_bathroom > 0.3:
        
            line = 'Number of visits to the bathroom, increase of: ' + str(round(percent_nr_visits_bathroom*100))+ '%; ' + str(nr_visits_bathroom) + "\n"
                   
            if (self.comorbiditesUrinary > 0) or (self.incontinence > 0):
                line1 = 'As the patient has also some urinary problems, a visit to the professional is indicated.'              
                   
        elif percent_nr_visits_bathroom > 0.1:
                
            line = 'Number of visits to the bathroom, increase of: ' + str(round(percent_nr_visits_bathroom*100))+ '%; ' + str(nr_visits_bathroom) + "\n"
                   
        elif percent_nr_visits_bathroom < -0.1:
            line = 'Number of visits to the bathroom, decrease of: ' + str(round(-percent_nr_visits_bathroom*100))+ '%; ' + str(nr_visits_bathroom) + "\n"
           
        else:
            line = 'Number of visits to the bathroom, no deviations; '  + str(nr_visits_bathroom) + "\n"
        print line
            
        line = '\t\t\"visitBathroom\":{\n' + '\t\t\t\"result\":' + str(round(percent_nr_visits_bathroom*100)) + ',\n' +'\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,nr_visits_bathroom))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
        
        incontinence = self.incontinence
        
        line = '\t\t\"incontinence\":'+str(incontinence) + ', \n'
        outputFile.writelines(line)

        if(percent_nr_visits_bathroom>=0):            
            probabilityIncontinence_visitsBathroom = 0.7*(percent_nr_visits_bathroom)
        else:
            # for decreasing number of visits to the bathroom the probability of Parkinson events is very low
            probabilityIncontinence_visitsBathroom = 0.01 
        probabilityIncontinence_medicalCondition = 0.3*incontinence    
        incontinenceProb = probabilityIncontinence_medicalCondition + probabilityIncontinence_visitsBathroom                        
        
        #plot a graph of the number of visits to the bathroom over the investigated days
        showGraph_bathroom = 0
        if showGraph_bathroom:
            #fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(nr_visits_bathroom)),int(max(nr_visits_bathroom))]
            plt.plot(nr_visits_bathroom,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of visits to the bathroom over the investigated days')
            plt.show()
        
        #assess the deviations in the time spent on digital devices
        time_dit = self.digitalTime
        maxValue = max(time_dit)        
        if maxValue>0:
            time_dit_ = time_dit/maxValue
        else:
            time_dit_ = time_dit

        time_dit1 = np.mean(time_dit_[:halfInterval])
        time_dit2 = np.mean(time_dit_[halfInterval:])
      
        percent_time_dit = time_dit2 - time_dit1 
        
        if percent_time_dit > 0.3:
        
            line = 'Time spent on digital devices, increase of: ' + str(round(percent_time_dit*100))+ '%; ' + str(time_dit) + "\n"
            print line         
            #outputFile.writelines(line)        
        
        elif percent_time_dit > 0.1:
                
            line = 'Time spent on digital devices, increase of: ' + str(round(percent_time_dit*100))+ '%; ' + str(time_dit) + "\n" 
                    
        elif percent_time_dit < -0.1:
            line = 'Time spent on digital devices, decrease of: ' + str(round(-percent_time_dit*100))+ '%; ' + str(time_dit) + "\n" 
            
        else:
            line = 'Time spent on digital devices, no deviations; '+ str(time_dit) + "\n" 
        print line
                
        line = '\t\t\"digitalTimeSpent\":{\n' + '\t\t\t\"result\":' + str(round(percent_time_dit*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,time_dit))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
        
        if(percent_time_dit>=0):            
            probabilityDigitalAddiction_timeDit = 0.6*(percent_time_dit)
            probabilityApathy_timeDit = 0.2*(percent_time_dit)            
        else:
            # for decreasing digital time usage the probability of addiction is very low
            probabilityDigitalAddiction_timeDit = 0.01 
            probabilityApathy_timeDit = 0.01

        probabilityDigitalAddiction_depression = 0.3*self.depression
        probDigitalAddiction = probabilityDigitalAddiction_depression + probabilityDigitalAddiction_timeDit      
        
        #plot a graph of the time spent on dit over the investigated days
        showGraph_time = 0
        if showGraph_time:
            #fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(time_dit)),int(max(time_dit))]
            plt.plot(time_dit,'ro')
            plt.axis(days_axis)
            plt.xlabel('Amount of time spent on the digital platform over the investigated days')
            plt.show()
        
        #assess deviations in the number of dit abnormal behaviours
        nr_abnormal_dit_behaviours = self.abnormalDigitalEvents
        maxValue = max(nr_abnormal_dit_behaviours)
        if maxValue>0:
            nr_abnormal_dit_behaviours_ = nr_abnormal_dit_behaviours/maxValue
        else:
            nr_abnormal_dit_behaviours_ = nr_abnormal_dit_behaviours

        abnormal_dit1 = np.mean(nr_abnormal_dit_behaviours_[:halfInterval])
        abnormal_dit2 = np.mean(nr_abnormal_dit_behaviours_[halfInterval:])

        percent_abnormal_dit = abnormal_dit2 - abnormal_dit1 
        
        if percent_abnormal_dit > 0.3:
        
            line = 'Number of abnormal digital behaviours, increase of: '+ str(round(percent_abnormal_dit*100))+ '%; ' + str(nr_abnormal_dit_behaviours) + "\n" 
            
            if (self.comorbiditesNeurologist > 0):
                line1 = 'A visit would be indicated to the professional in charge of the patient, due to an increase in the digital abnormal behaviour. \n'
                print line1
                            
        elif percent_abnormal_dit > 0.1:
                
            line = 'Number of abnormal digital behaviours, increase of: ' + str(round(percent_abnormal_dit*100))+ '%; ' + str(nr_abnormal_dit_behaviours) + "\n" 
                    
        elif percent_abnormal_dit < -0.1:
            line = 'Number of abnormal digital behaviours, decrease of: ' + str(round(-percent_abnormal_dit*100))+ '%; ' + str(nr_abnormal_dit_behaviours) + "\n" 
            
        else:
            line = 'Number of abnormal digital behaviours, no deviations; '  + str(nr_abnormal_dit_behaviours) + "\n" 
        print line
             
        line = '\t\t\"abnormalDigitalBehaviours\":{\n' + '\t\t\t\"result\":' + str(round(percent_abnormal_dit*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,nr_abnormal_dit_behaviours))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)

        if(percent_abnormal_dit>=0):            
            probabilityDigitalConfusion_abnormalDigitalBehaviour = percent_abnormal_dit
            probabilityImprovedBehaviour_abnormalDigitalBehaviour = 0.001
        else:
            # for decreasing number of abnormal digital events the probability of digital confusion is very low
            probabilityDigitalConfusion_abnormalDigitalBehaviour = 0.01 
            probabilityImprovedBehaviour_abnormalDigitalBehaviour = -0.2*percent_abnormal_dit         

	     #plot a graph of the digital abnormal behaviours over the investigated days
        showGraph_abnormal = 0
        if showGraph_abnormal:
            #fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(nr_abnormal_dit_behaviours)),int(max(nr_abnormal_dit_behaviours))]
            plt.plot(nr_abnormal_dit_behaviours,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of digital abnormal behaviours events over the investigated days')
            plt.show()   

        cognitiveFunctions = self.cognitiveFunctions
        if(cognitiveFunctions):
            probabilityDigitalConfusion_abnormalDigitalBehaviour = 0.6*probabilityDigitalConfusion_abnormalDigitalBehaviour		
            probDigitalConfusion = probabilityDigitalConfusion_abnormalDigitalBehaviour
        else:
            probabilityDigitalConfusion_abnormalDigitalBehaviour = 0.7*probabilityDigitalConfusion_abnormalDigitalBehaviour		
            probDigitalConfusion = 0.7*percent_abnormal_dit + 0.3*(1-int(cognitiveFunctions))
        
        probabilityInsomnia_digitalAddiction = 0.2*probDigitalAddiction
        probabilityInsomnia_depression = 0.2*self.depression
        probabilityInsomnia_medicalCondition = 0.3*insomnia
        insomniaProb = probabilityInsomnia_medicalCondition + probabilityInsomnia_nightMotion + probabilityInsomnia_depression + probabilityInsomnia_digitalAddiction
        if(insomniaProb>1):
            insomniaProb = 0.9
        
        line = '\t\t\"probabilities\":[\n' 
        outputFile.writelines(line)
       
        line = '\t\t{\n\t\t\t\"type\":\"confusion|abnormalEvents\",\n'+'\t\t\t\"value\":'+str(round(probabilityConfusion_abnormalEvents,3)) + '\n\t\t},\n'
        outputFile.writelines(line)   
        
        line = '\t\t{\n\t\t\t\"type\":\"confusion|psychiatricComorbidites\",\n'+'\t\t\t\"value\":'+str(round(probabilityComorbiditesPsychiatrist,3)) + '\n\t\t},\n'
        outputFile.writelines(line)   
        
        line = '\t\t{\n\t\t\t\"type\":\"confusion|neurologicComorbidites\",\n'+'\t\t\t\"value\":'+str(round(probabilityComorbiditesNeurologist,3)) + '\n\t\t},\n'
        outputFile.writelines(line)   
        
        line = '\t\t{\n\t\t\t\"type\":\"Confusion\",\n'+'\t\t\t\"value\":'+str(round(probConfusion,3)) + '\n\t\t},\n'       
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Insomnia|nightMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityInsomnia_nightMotion,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Insomnia|digitalAddiction\",\n'+'\t\t\t\"value\":'+str(round(probabilityInsomnia_digitalAddiction,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Insomnia|depression\",\n'+'\t\t\t\"value\":'+str(round(probabilityInsomnia_depression,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Insomnia|medicalCondition\",\n'+'\t\t\t\"value\":'+str(round(probabilityInsomnia_medicalCondition,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"sleepDisorders\",\n'+'\t\t\t\"value\":'+str(round(insomniaProb,3)) + '\n\t\t},\n'
        outputFile.writelines(line)        
        
        line = '\t\t{\n\t\t\t\"type\":\"Incontinence|visitsBathroom\",\n'+'\t\t\t\"value\":'+str(round(probabilityIncontinence_visitsBathroom,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Incontinence|nedicalCondition\",\n'+'\t\t\t\"value\":'+str(round(probabilityIncontinence_medicalCondition,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Incontinence\",\n'+'\t\t\t\"value\":'+str(round(incontinenceProb,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Hipertension|biologicalMeasurements\",\n'+'\t\t\t\"value\":'+str(round(probabilityHipertension_hr,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Hipertension|medicalCondition\",\n'+'\t\t\t\"value\":'+str(round( probabilityHipertension_medicalCondition,3)) + '\n\t\t},\n'
        outputFile.writelines(line)  

        line = '\t\t{\n\t\t\t\"type\":\"Hipertension\",\n'+'\t\t\t\"value\":'+str(round(hipertensionProb,3)) + '\n\t\t},\n'
        outputFile.writelines(line)              
        
        line = '\t\t{\n\t\t\t\"type\":\"Cardiovascular condition|biologicalMeasurements\",\n'+'\t\t\t\"value\":'+str(round(probabilityCardiovascular_hr,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Cardiovascular condition|medicalCondition\",\n'+'\t\t\t\"value\":'+str(round(probabilityCardiovascular_medicalCondition,3)) + '\n\t\t},\n'
        outputFile.writelines(line)  

        line = '\t\t{\n\t\t\t\"type\":\"Cardiovascular condition\",\n'+'\t\t\t\"value\":'+str(round(cardiovascularProb,3)) + '\n\t\t},\n'
        outputFile.writelines(line)  
        
        line = '\t\t{\n\t\t\t\"type\":\"digitalAddiction|digitalTimeUsage\",\n'+'\t\t\t\"value\":'+str(round(probabilityDigitalAddiction_timeDit,3)) + '\n\t\t},\n'
        outputFile.writelines(line)            
        
        line = '\t\t{\n\t\t\t\"type\":\"digitalAddiction|depression\",\n'+'\t\t\t\"value\":'+str(round(probabilityDigitalAddiction_depression,3)) + '\n\t\t},\n'
        outputFile.writelines(line)            

        line = '\t\t{\n\t\t\t\"type\":\"digitalAddiction\",\n'+'\t\t\t\"value\":'+str(round(probDigitalAddiction,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"digitalConfusion|abnormalDigitalBehaviour\",\n'+'\t\t\t\"value\":'+str(round(probabilityDigitalConfusion_abnormalDigitalBehaviour,3)) + '\n\t\t},\n'
        outputFile.writelines(line)   
        
        line = '\t\t{\n\t\t\t\"type\":\"digitalConfusion\",\n'+'\t\t\t\"value\":'+str(round(probDigitalConfusion,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
                       
        probApathy = probabilityApathy_stationary + probabilityApathy_leavingHouse + probabilityApathy_timeDit+probabilityApathy_dailyMotion+probabilityApathy_steps                      
    
        line = '\t\t{\n\t\t\t\"type\":\"Apathy|stationaryBehaviour\",\n'+'\t\t\t\"value\":'+str(round(probabilityApathy_stationary,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Apathy|dailyMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityApathy_dailyMotion,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Apathy|overallMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityApathy_steps,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Apathy|leavingHouse\",\n'+'\t\t\t\"value\":'+str(round(probabilityApathy_leavingHouse,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Apathy|digitalTimeUsage\",\n'+'\t\t\t\"value\":'+str(round(probabilityApathy_timeDit,3)) + '\n\t\t},\n'
        outputFile.writelines(line)

        line = '\t\t{\n\t\t\t\"type\":\"Apathy\",\n'+'\t\t\t\"value\":'+str(round(probApathy,3)) + '\n\t\t},\n'
        outputFile.writelines(line)                               
        
        probMovementIssues = probabilityMovementIssues_fall_down  + probabilityMovementIssues_lossBalance + probabilityMovementIssues_leavingHouse + probabilityMovementIssues_stationary + probabilityMovementIssues_dailyMotion + probabilityMovementIssues_steps
        
        line = '\t\t{\n\t\t\t\"type\":\"MovementIssues|fallDown\",\n'+'\t\t\t\"value\":'+str(round(probabilityMovementIssues_fall_down,3)) + '\n\t\t},\n'      
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"MovementIssues|lossOfBalance\",\n'+'\t\t\t\"value\":'+str(round(probabilityMovementIssues_lossBalance,3)) + '\n\t\t},\n'      
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"MovementIssues|stationaryBehaviour\",\n'+'\t\t\t\"value\":'+str(round(probabilityMovementIssues_stationary,3)) + '\n\t\t},\n'      
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"MovementIssues|dailyMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityMovementIssues_dailyMotion,3)) + '\n\t\t},\n'      
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"MovementIssues|overallMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityMovementIssues_steps,3)) + '\n\t\t},\n'      
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"MovementIssues|leavingHouse\",\n'+'\t\t\t\"value\":'+str(round(probabilityMovementIssues_leavingHouse,3)) + '\n\t\t},\n'      
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"MovementIssues\",\n'+'\t\t\t\"value\":'+str(round(probMovementIssues,3)) + '\n\t\t},\n'
        outputFile.writelines(line)                
        
        probImprovedBehaviour = probabilityImprovedBehaviour_abnormalDigitalBehaviour + probabilityImprovedBehaviour_dailyMotion + probabilityImprovedBehaviour_fallDown + probabilityImprovedBehaviour_abnormalEvents + probabilityImprovedBehaviour_lossBalance + probabilityImprovedBehaviour_nightMotion + probabilityImprovedBehaviour_stationary + probabilityImprovedBehaviour_leavingHouse + probabilityImprovedBehaviour_steps
        
        if(probImprovedBehaviour>1):
            probImprovedBehaviour = 1
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|confusedBehaviours\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_abnormalEvents,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|stationary\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_stationary,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|dailyMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_dailyMotion,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|overallMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_steps,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|nightMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_nightMotion,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|leavingHouse\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_leavingHouse,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|fallDown\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_fallDown,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)

        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|lossOfBalance\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_lossBalance,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour|abnormalDigitalBehaviour\",\n'+'\t\t\t\"value\":'+str(round(probabilityImprovedBehaviour_abnormalDigitalBehaviour,3)) + '\n\t\t},\n'                                    
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"ImprovedBehaviour\",\n'+'\t\t\t\"value\":'+str(round(probImprovedBehaviour,3)) + '\n\t\t}\n'                                    
        outputFile.writelines(line)  
        
        line = '\t\t]\n'
        outputFile.writelines(line)        
          
        
    def multimodalFusionalgorithms(self,outputFile,patientId,currentDate,investigatedPeriodinDays,inputFileEHR,inputFileHETRA,inputFileDIT):
    
        commentsEnabled = 1        
        # currentDay = currentDate.day
        startDate = currentDate + timedelta(days=-investigatedPeriodinDays)
              
        # parse the EHR File
        foundPatient, main_diagnosis, disease_level, age, gender, civilStatus, bmi, active, mobility, gradeDependence, autonomousWalk, independenceDailyActivities, comorbiditesNeurologist, comorbiditesPsychiatrist, cognitiveFunctions, comorbiditesCardiovascular, hipertension, comorbiditesUrinary, incontinence, insomnia, depression, medications, medicationName, evaluations, evaluationsScore, evaluationDates, evaluationDateList  = self.parseEHRFile(inputFileEHR,patientId,investigatedPeriodinDays,startDate,currentDate)
     
        if(foundPatient):
            self.mainDiagnose = main_diagnosis # the main diagnose is 1 for Parkinson's and 0 for Alzheimer's 
            self.disease_level = disease_level
            self.insomnia = insomnia
            self.incontinence = incontinence
            self.depression = depression
            self.comorbiditesNeurologist = comorbiditesNeurologist
            self.comorbiditesUrinary= comorbiditesUrinary
            self.comorbiditesPsychiatrist= comorbiditesPsychiatrist
            self.comorbiditesCardiovascular = comorbiditesCardiovascular       
            self.hipertension = hipertension
            self.cognitiveFunctions = cognitiveFunctions  
            self.medications = medications
            self.medicationName = medicationName
            self.evaluationsExercises = evaluations
            self.evaluationsScore = evaluationsScore
            self.evaluationDates = evaluationDates
            self.evaluationDateList = evaluationDateList            
       
            
            if self.mainDiagnose==1:
                str_patient = 'The patient with id '+str(patientId)+ ' has Parkinsons level ' + str(self.disease_level)  
                if commentsEnabled: 
                    print str_patient
            elif (self.mainDiagnose==0):
                str_patient = 'The patient with id '+str(patientId)+ ' has Alzheimers level ' + str(self.disease_level)  
                if commentsEnabled: 
                    print str_patient

#            line = '\t{\n'+'\t\t\"patientID\":\"'+str(patientId)+ '\",\n'
#            outputFile.writelines(line)
#    
#            line = '\t\t\"startDate\":\"' + str(startDate) + '\",\n' 
#            outputFile.writelines(line)
#            line = '\t\t\"endDate\":\"' + str(currentDate) + '\",\n' 
#            outputFile.writelines(line)
          
            
            # call the digital abnormal behaviour module for finding the number of abnormal events and the total interaction time  
            ## current implementation of the DIT
            inputDITpath = '../input/DIT'
            date_from = str(startDate) 
            date_to = str(currentDate)                   
            print date_from
            print date_to
            
            # parameters for DIT analysis
            time_dit = np.zeros(shape= (investigatedPeriodinDays))
            nr_abnormalBehaviours_S = np.zeros(shape= (investigatedPeriodinDays))
            nr_abnormalBehaviours_T = np.zeros(shape= (investigatedPeriodinDays))
            nr_abnormalBehaviours_ST = np.zeros(shape= (investigatedPeriodinDays))
            nr_abnormal_dit_behaviours = np.zeros(shape= (investigatedPeriodinDays))
            
            inputDITABDFiletoMF = inputDITpath + '/' + 'inputEventABDfile_.txt'    
            typeAnalysis = "ABD"
            response_abd = getDIT.get_data(patientId, date_from, date_to, inputDITABDFiletoMF,typeAnalysis)                                                                                             
            if response_abd>0:
                timeABD_dit, nr_abnormal_dit_behaviours, nr_abnormalBehaviours_S, nr_abnormalBehaviours_T, nr_abnormalBehaviours_ST = self.parseDITFile_ABD(inputDITABDFiletoMF,investigatedPeriodinDays,startDate.day)                                    
                print "Dit abnormal events parsed"
            else:           
                print "No file received in DIT with abnormal events"          
                
            inputDITEventFiletoMF = inputDITpath + '/' + 'inputEventfile_.txt'    
            typeAnalysis = "Event"
            response_event = getDIT.get_data(patientId, date_from, date_to, inputDITEventFiletoMF,typeAnalysis)                                                                                             
            if response_event>0:
                time_dit = self.parseDITFile_allEvents(inputDITEventFiletoMF,investigatedPeriodinDays,startDate.day)        
                print "Dit events parsed"
            else:           
                print "No file received in DIT with events"          
                          
            # extract the ABD parameters for each of the investigated day in the predefined period
            stationary = np.zeros(shape= (investigatedPeriodinDays))
            dailyMotion = np.zeros(shape= (investigatedPeriodinDays))
            nr_visits_bathroom = np.zeros(shape= (investigatedPeriodinDays))
            nr_leaving_the_house = np.zeros(shape= (investigatedPeriodinDays))
    
            freezing_events = np.zeros(shape= (investigatedPeriodinDays))
            festination_events = np.zeros(shape= (investigatedPeriodinDays))
            loss_of_balance_events = np.zeros(shape= (investigatedPeriodinDays))
            fall_down_events = np.zeros(shape= (investigatedPeriodinDays))
            abnormalEvents = np.zeros(shape= (investigatedPeriodinDays))
            nr_night_visits = np.zeros(shape= (investigatedPeriodinDays))
            
            heart_rate_min = np.zeros (shape= (investigatedPeriodinDays))
            heart_rate_max = np.zeros (shape= (investigatedPeriodinDays))
            heart_rate_mean = np.zeros (shape= (investigatedPeriodinDays))
            heart_rate_median = np.zeros (shape= (investigatedPeriodinDays))
            heart_rate_mode = np.zeros (shape= (investigatedPeriodinDays))
            heart_rate_skewness = np.zeros (shape= (investigatedPeriodinDays))
            heart_rate_kurtosis = np.zeros (shape= (investigatedPeriodinDays))
            
            heartRateLow = np.zeros (shape= (investigatedPeriodinDays))
            heartRateHigh = np.zeros (shape= (investigatedPeriodinDays))
            steps = np.zeros (shape= (investigatedPeriodinDays))
            gsr_min = np.zeros (shape= (investigatedPeriodinDays))
            gsr_max = np.zeros (shape= (investigatedPeriodinDays))
            gsr_mean = np.zeros (shape= (investigatedPeriodinDays))
            gsr_median = np.zeros (shape= (investigatedPeriodinDays))
            gsr_mode = np.zeros (shape= (investigatedPeriodinDays))
            gsr_skewness = np.zeros (shape= (investigatedPeriodinDays))
            gsr_kurtosis = np.zeros (shape= (investigatedPeriodinDays))
            #movement_evolution_events = np.zeros(shape= (investigatedPeriodinDays))                  
                     
            foundPatientId, stationary, dailyMotion, freezing_events, festination_events, loss_of_balance_events, fall_down_events, nr_visits_bathroom, nr_leaving_the_house, nr_night_visits, abnormalEvents, heart_rate_min, heart_rate_max, heart_rate_mean, heart_rate_mode, heart_rate_median, heart_rate_kurtosis, heart_rate_skewness, heartRateLow, heartRateHigh, gsr_min, gsr_max, gsr_mean, gsr_mode, gsr_median, gsr_kurtosis, gsr_skewness, steps  = self.parseHETRAFile(inputFileHETRA,patientId,startDate,investigatedPeriodinDays)                                                                                                    
            
            if(foundPatientId>0):
				self.stationaryEvents = stationary
				self.abnormalEvents = abnormalEvents
				self.dailyMotion = dailyMotion
				self.freezing = freezing_events
				self.festination = festination_events
				self.nightMotion = nr_night_visits
				self.fallDown = fall_down_events
				self.lossOfBalance = loss_of_balance_events
				self.visitsBathroom = nr_visits_bathroom
				self.leavingHouse = nr_leaving_the_house
				self.digitalTime = time_dit
				self.abnormalDigitalEvents = nr_abnormal_dit_behaviours
				self.heartRate_mean = heart_rate_mean
				self.heartRate_min = heart_rate_min
				self.heartRate_max = heart_rate_max
				self.heartRate_median = heart_rate_median
				self.heartRate_mode = heart_rate_mode
				self.heartRate_skewness = heart_rate_skewness
				self.heartRate_kurtosis= heart_rate_kurtosis
				self.heartRateLow = heartRateLow  # the number of events is considered
				self.heartRateHigh = heartRateHigh # the number of events is considered
				self.steps = steps
				self.galvanicSkinResponse_mean = gsr_mean
				self.galvanicSkinResponse_min = gsr_min
				self.galvanicSkinResponse_max = gsr_max
				self.galvanicSkinResponse_mode = gsr_mode
				self.galvanicSkinResponse_median = gsr_median
				self.galvanicSkinResponse_skewness = gsr_skewness
				self.galvanicSkinResponse_kurtosis = gsr_kurtosis
				
				#Different sets of functionalities are evaluated in the case of Parkinson's or Alzheimer's disease
				if(self.mainDiagnose==1):
					self.evaluateParkinsonsActivities(outputFile,investigatedPeriodinDays)
				elif(self.mainDiagnose==0):
					self.evaluateAlzheimersActivities(outputFile,investigatedPeriodinDays)
				else:
					print "A correct diagnosis wasn't found. The analysis will not be performed.\n"
                    
            else:              
                print 'The HETRA data for patient with id: ' + str(patientId) + ' was not found.'
        else:
            print 'The EHR data for patient with id: ' + str(patientId) + ' was not found.'

if __name__ == '__main__':

	# define the set of parameters
	#the list of patienIds need to be updated
    listPatientIds = ['5315e0fb-a7ef-4742-9387-12cd9a000b20','50baff5b-7898-436d-8eb6-543600cc86c3']
    	
    nrPatients = len(listPatientIds)
    investigatedPeriodinDays = 10  #interval for MF analysis
    analysisDate = datetime.date.today()
	
    str_date = analysisDate.strftime('%d-%m-%Y')
    #analysisDate = analysisDate.replace(2018,6,11) #this date is used for testing purposes
    analysisDate = analysisDate.replace(2018,7,21) #this date is used for testing purposes
    
    year = analysisDate.year
    month= analysisDate.month
    day = analysisDate.day
    
    #output file of the MF module containing the results of the analysis
    outputMFpath = '../output/ehr'
    inputEHRpath = '../input/EHR'
    inputHETRApath = '../input/HETRA'
    inputDITpath = '../input/DIT'
    
    if(day<10):
        dayString = '0'+str(day)
    else:
        dayString = str(day)
    if(month<10):
        monthString = '0'+str(month)
    else:
        monthString = str(month)
        
    outputMF_File =  'MF_' + str(year) + monthString + dayString  + '.json'
    inputEHR_File = 'EHR_' + str(year) + monthString + dayString  + '.json'
    inputHETRA_File = 'HETRA_' + str(year) + monthString + dayString  + '.json'
    inputDIT_File =   'DitML_' + str(year) + monthString + dayString  + '.json'
                                       
    outputFileMF = outputMFpath + '/' + outputMF_File   
    
    #check if all the input files are available
    inputFileEHR = inputEHRpath + '/' + inputEHR_File   
    inputFileHETRA = inputHETRApath + '/' + inputHETRA_File   
    inputFileDIT = inputDITpath + '/' + inputDIT_File
        
    startDate = analysisDate + timedelta(days=-investigatedPeriodinDays)	   
    
    if (os.path.isfile(inputFileEHR) & os.path.isfile(inputFileHETRA) & os.path.isfile(inputFileDIT)):
    
        print 'all input files are received'
        outputFile = open(outputFileMF,'w')     
        line = '[\n'
        outputFile.writelines(line)	
        
        for i in range(nrPatients):
            patientId = listPatientIds[i]  
            line = '\t{\n'+'\t\t\"patientID\":\"'+str(patientId)+ '\",\n'
            outputFile.writelines(line)
    
            line = '\t\t\"startDate\":\"' + str(startDate) + '\",\n' 
            outputFile.writelines(line)
            line = '\t\t\"endDate\":\"' + str(analysisDate) + '\",\n' 
            outputFile.writelines(line)
            
            mf=MultimodalFusion()
            mf.multimodalFusionalgorithms(outputFile,patientId,analysisDate,investigatedPeriodinDays,inputFileEHR,inputFileHETRA,inputFileDIT)        
            if(i==nrPatients-1):
                line = '\t}\n'                
            else:
                line = '\t},\n'                                
            outputFile.writelines(line)  
        
        #close the MF output file
        line = ']'
        outputFile.writelines(line)    
        outputFile.close()  
        
        # upload the output file to the cloud containing the analysis results
        uploadResults = 0
        if(uploadResults):
        
            outputPath= '../output'        
            outFilePath =  outputPath + '/ehr' + '/' + outputMF_File
            uploadFileToCloud.uploadFile_Cloud(outFilePath,outputMF_File)
    
        print('Multimodal Fusion module completed.')    
        
    else:
        print 'not all input files are received, analysis is postponed'
        