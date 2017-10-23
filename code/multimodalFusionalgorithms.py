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
       
class MultimodalFusion():
    
    def __init__(self,mainDiagnose=0,stationaryEvents=[],disease_level=0,dailyMotion=[],nightMotion=[],visitsBathroom=[],abnormalEvents=[],freezing=[],festination=[],lossOfBalance=[],fallDown=[],incontinence=[],leavingHouse=[],digitalTime=[],abnormalDigitalEvents=[],insomnia=0,comorbiditesNeurologist=0,comorbiditesUrinary=0,cognitiveFunctions=0,comorbiditesPsychiatrist=0):
        
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
        self.digitalTime = digitalTime
        self.abnormalDigitalEvents = abnormalDigitalEvents    
        self.insomnia = insomnia      
        self.comorbiditesNeurologist = comorbiditesNeurologist
        self.comorbiditesUrinary= comorbiditesUrinary
        self.comorbiditesPsychiatrist= comorbiditesPsychiatrist
        self.cognitiveFunctions = cognitiveFunctions
              
    def parseABDFile(self,filePath):
       
        stationary_=0
        dailyMov =0
        freezing_nr =0
        festination_nr = 0
        loss_of_balance_nr =0
        fall_down_nr = 0
        nr_visits_bathroom = 0
        leaving_the_house = 0
        nr_night_visits = 0
                   
        with open(filePath,'r') as inf:
            for line in inf:          
          
                functionalityName = line.split(':')[0]              
                obj = line.split('\t')[1]     
              
                if functionalityName == 'daily_motion':
                   
                    daily_dict = ast.literal_eval(obj)
                    stationary_ = int(daily_dict.get('stationary',0))
                    fastMov = daily_dict.get('fast_mov',0)  
                    slowMov = daily_dict.get('slow_mov',0)  
                    dailyMov = fastMov + slowMov        
                                  
                elif functionalityName == 'as_day_motion':
           
                    daily_dict = ast.literal_eval(obj)
                    
                    toilet_list = daily_dict.get('toilet',0)  
                    toilet_times = toilet_list[0]
                    toilet_duration = toilet_list[1]         
                         
                    entrance_list = daily_dict.get('entrance',0)  
                    entrance_times = entrance_list[0]
                    entrance_duration = entrance_list[1]         
                    
                    bedroom_list = daily_dict.get('bedroom',0)  
                    bedroom_times = bedroom_list[0]
                    bedroom_duration = bedroom_list[1]         
                      
                elif functionalityName == 'as_night_motion':
           
                    daily_dict = ast.literal_eval(obj)
                    nr_night_visits = 0 
                    toilet_list = daily_dict.get('toilet',0)  
                    toilet_times = toilet_list[0]
                    toilet_duration = toilet_list[1]         
                
                    if (toilet_times!=[]):                      
                        nr_night_visits = nr_night_visits + len(toilet_list)/2
                     
                    entrance_list = daily_dict.get('entrance',0)  
                    entrance_times = entrance_list[0]
                    #entrance_duration = entrance_list[1]  

                    if (entrance_times!=[]):                      
                        nr_night_visits = nr_night_visits + len(entrance_list)/2
           
                    bedroom_list = daily_dict.get('bedroom',0)  
                    bedroom_times = bedroom_list[0]
                    bedroom_duration = bedroom_list[1]         
                    if (bedroom_times!=[]):                      
                        nr_night_visits = nr_night_visits + len(bedroom_list)/2                                                                 
                       
                elif functionalityName == 'freezing':
           
                   daily_dict = ast.literal_eval(obj)
        
                   freezing_nr = daily_dict.get('number',0)  
                   freezing_beginning = daily_dict.get('beggining',0)  
                   freezing_duration = daily_dict.get('duration',0)        
                   
                elif functionalityName == 'festination':
           
                   daily_dict = ast.literal_eval(obj)
        
                   festination_nr = daily_dict.get('number',0)  
                   festination_beginning = daily_dict.get('beggining',0)  
                   festination_duration = daily_dict.get('duration',0)    
           
                elif functionalityName == 'loss_of_balance':
           
                   daily_dict = ast.literal_eval(obj)
        
                   loss_of_balance_nr = daily_dict.get('number',0)  
                   loss_of_balance_beginning = daily_dict.get('beggining',0)  
                   loss_of_balance_duration = daily_dict.get('duration',0)    
           
                elif functionalityName == 'fall_down':
               
                   daily_dict = ast.literal_eval(obj)
        
                   fall_down_nr = daily_dict.get('number',0)  
                   fall_down_beginning = daily_dict.get('beggining',0)  
                   fall_down_duration = daily_dict.get('duration',0)    
       
                elif functionalityName == 'visit_bathroom':
           
                    daily_dict = ast.literal_eval(obj)
                    
                    nr_visits_bathroom = daily_dict.get('number',0)  
                    toilet_beggining = daily_dict.get('beggining',0)  
                    toilet_duration = daily_dict.get('duration',0)            
                                                          
                elif functionalityName == 'confusion_behavior_detection':
           
                   daily_dict = ast.literal_eval(obj)
        
                   confusion_nr = daily_dict.get('number',0)  
                   #print confusion_nr
                   confusion_times = daily_dict.get('times',0)  
                   confusion_duration = daily_dict.get('duration',0)        
                   #print max(confusion_duration) 
           
                elif functionalityName == 'leave the house':  
           
                   leaving_the_house = obj
                   #print leaving_the_house
           
                elif functionalityName == 'leave_house_confused':  
          
                   confused_and_leaving_the_house = obj
                   #print confused_and_leaving_the_house
           
                else:
                   print line
            
            return stationary_, dailyMov, freezing_nr, festination_nr, loss_of_balance_nr, fall_down_nr, nr_visits_bathroom, leaving_the_house, nr_night_visits, confusion_nr    

    def parseEHRFile(self,filePath):
       
        with open(filePath,'r') as inf:
            for line in inf:          
          
                functionalityName = line.split(':')[0]
                #print functionalityName
                obj = line.split('\t')[1]     
              
                if functionalityName == 'Main_diagnosis':
           
                    diagnosis = obj
                    if diagnosis.find('Parkinsons') > 0:
                        main_diagnosis = 1
                    else:
                        main_diagnosis = 0               
               
                    #print main_diagnosis
           
                elif functionalityName == 'ParkinsonHoehnAndYard':           
                    disease_level = obj				
                elif functionalityName == 'MMSE':
                    mmse = int(obj)
                    if(mmse<=10):
    					  	 disease_level = 5
					   
                    elif(mmse<=19):
						    disease_level = 4
					   
                    elif(mmse<=24):
						    disease_level = 3
					   
                    elif(mmse<=27):
						    disease_level = 2
					   
                    else:
						    disease_level = 1
                    					
                elif functionalityName == 'Date_birth':  
           
                    datepatient = obj
                    datepatient = datepatient.replace('\n', '')
                    datepatient = datepatient.replace('\r', '')
                    datepatient = datepatient.replace('\'', '')
		    
                    date_birth = datetime.datetime.strptime(datepatient, "%Y-%m-%d")                 

                    currentDay =  datetime.date.today()
                    currentYear = currentDay.year
                    age = currentYear - date_birth.year           
                    #print age
           
                elif functionalityName == 'Gender':  
          
                    gender = obj
           
                elif functionalityName == 'CivilStatus':  
           
                    civil_Status = obj
                    if civil_Status.find('Single') > 0:
                        civilStatus = 0
                    elif civil_Status.find('Married') > 0:
                        civilStatus = 1
                    elif civil_Status.find('Divorced') > 0:
                        civilStatus = 2
                    else:
                        civilStatus = 3                
                        #print civilStatus    
                
                elif functionalityName == 'Bmi':  
          
                    bmi = obj           
       
                elif functionalityName == 'Active':  
           
                    active = obj
                      
                elif functionalityName == 'Mobility':  
          
                    mobility = obj
                  
                elif functionalityName == 'GradeDependence':  
           
                    gradeDependence = obj
                      
                elif functionalityName == 'AutonomousWalk':  
          
                    autonomousWalk = obj
           
                elif functionalityName == 'IndependenceDailyActivities':  
          
                    independenceDailyActivities = obj
       
                elif functionalityName == 'ComorbiditiesNeurologist':  
          
                    comorbiditesNeurologist = obj
           
                elif functionalityName == 'ComorbiditiesPsychiatrist':  
          
                    comorbiditesPsychiatrist = obj
           
                elif functionalityName == 'PreserveCognitiveFunctions':  
          
                    cognitiveFunctions = obj
           
                elif functionalityName == 'ComorbiditiesCardiovascular':  
          
                    comorbiditesCardiovascular = obj
           
                elif functionalityName == 'Hipertension':  
          
                    hipertension = obj
           
                elif functionalityName == 'ComorbiditiesUrinary':  
          
                    comorbiditesUrinary = obj
           
                elif functionalityName == 'Incontinence':  
          
                    incontinence = obj    
       
                elif functionalityName == 'Insomnia':  
          
                    insomnia = obj      
                #else:
                    #print obj
        
        return int(main_diagnosis), int(disease_level), int(age), int(gender), int(civilStatus), int(bmi), int(active), int(mobility), int(gradeDependence), int(autonomousWalk), int(independenceDailyActivities), int(comorbiditesNeurologist), int(comorbiditesPsychiatrist), int(cognitiveFunctions), int(comorbiditesCardiovascular), int(hipertension), int(comorbiditesUrinary), int(incontinence), int(insomnia) 

    def parseDITFile(self,filePath):
       
        with open(filePath,'r') as inf:
            for line in inf:          
          
                functionalityName = line.split(':')[0]
                #print functionalityName
                obj = line.split('\t')[1]     
              
                if functionalityName == 'total_time_dit':
           
                    time_dit = obj            
           
                elif functionalityName == 'new_attachments':
           
                   dit_dict = ast.literal_eval(obj)
        
                   nr_abnormal_behaviours_attachment = dit_dict.get('number',0)  
                   attachement_beggining = dit_dict.get('beggining',0)  
                   attachment_duration = dit_dict.get('duration',0)   
               
                elif functionalityName == 'add_medication':
           
                   dit_dict = ast.literal_eval(obj)
        
                   nr_abnormal_behaviours_medication = dit_dict.get('number',0)             
                   medication_beggining = dit_dict.get('beggining',0)  
                   medication_duration = dit_dict.get('duration',0)   
           
                elif functionalityName == 'add_appointment':
           
                   dit_dict = ast.literal_eval(obj)
        
                   nr_abnormal_behaviours_appointment = dit_dict.get('number',0)  
                   appointment_beggining = dit_dict.get('beggining',0)  
                   appointment_duration = dit_dict.get('duration',0)   
           
                else:
                    print line
           
            return time_dit, nr_abnormal_behaviours_attachment, nr_abnormal_behaviours_medication, nr_abnormal_behaviours_appointment   
    
    def parseDITFile_allEvents(self,filePath):
    
        abnormalUsageTime = 0
        nrAbnormalEvents = 0
        type_events_T = 0
        type_events_S = 0
        type_events_ST = 0
        nrFunctionCalls_newAttachment = 0
        nrFunctionCalls_kBase = 0
        nrFunctionCalls_medication = 0 
        
        with open(filePath,'r') as inf:
        
            for line in inf:          
          
                functionalityName = line
              
                if functionalityName.find("doctype") > 0 :
           
                    fieldName = functionalityName.split(':')[1]
                    obj = fieldName.split(',')[0]
                    nrAbnormalEvents = nrAbnormalEvents + 1
           
                    if obj.find("ST") > 0:
                        type_events_ST = type_events_ST + 1 
                    elif obj.find("S") > 0:
                        type_events_S = type_events_S + 1 
                    elif obj.find("T") > 0:
                        type_events_T = type_events_T + 1     
           
                elif functionalityName.find("elapsedTime") > 0:
           
                    fieldName = functionalityName.split(':')[1]
                    obj = fieldName.split(',')[0]
                    
                    abnormalUsageTime = abnormalUsageTime + int(obj)
                    #print abnormalUsageTime
           
                elif functionalityName.find("function") > 0:
           
                    fieldName = functionalityName.split(':')[1]
                    obj = fieldName.split(',')[0]           
                    if obj.find("NEW_ATTACHMENT") > 0:
                        nrFunctionCalls_newAttachment = nrFunctionCalls_newAttachment + 1 
                    elif obj.find("K_BASE") > 0:
                        nrFunctionCalls_kBase = nrFunctionCalls_kBase + 1                            
                    elif obj.find("FORM_MEDICACION") > 0:
                        nrFunctionCalls_medication = nrFunctionCalls_medication + 1  
    
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
        
        line = '\t\"stationaryBehaviour\":{\n' + '\t\t\"result\":' + str(round(percent_stationary*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,stationary))+']\n' + '\t},\n'
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
                
        line = '\t\"dailyMotion\":{\n' + '\t\t\"result\":' + str(round(percent_dailyMotion*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,dailyMotion))+']\n' + '\t},\n'
        outputFile.writelines(line)
        
        #in the case daily motion decreases, the probability of apathy increases
        if(percent_dailyMotion<0):
            probabilityApathy_dailyMotion = -percent_dailyMotion*0.3
            probabilityImprovedBehaviour_dailyMotion = 0.001
        else:
            # for increasing daily motion the probability of apathy is very low
            probabilityApathy_dailyMotion = 0.001
            probabilityImprovedBehaviour_dailyMotion= 0.3*percent_dailyMotion
            
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
    
        line = '\t\"leavingHouse\":{\n' + '\t\t\"result\":' + str(round(percent_leavingHouse*100)) + ',\n' + '\t\t\"events\":[' +','.join(map(str,nr_leaving_the_house))+']\n' + '\t},\n'
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
        
        line = '\t\"nightMotion\":{\n' + '\t\t\"result\":' + str(round(percent_nightMotion*100)) + ',\n' + '\t\t\"events\":[' +','.join(map(str,nr_night_visits))+']\n' + '\t},\n'
        outputFile.writelines(line)
    
        insomnia = self.insomnia
        line = '\t\"insomnia\":'+str(insomnia)+',\n'
        outputFile.writelines(line)
    
        if(percent_nightMotion>=0):
            probabilityInsomnia_nightMotion = percent_nightMotion
            probabilityImprovedBehaviour_nightMotion = 0.001            
        else:
            # for decreasing night motion the probability of insomnia is very low
            probabilityInsomnia_nightMotion = 0.001
            probabilityImprovedBehaviour_nightMotion = -0.2*percent_nightMotion
                      
        if(insomnia):
            probabilityInsomnia_nightMotion = 0.5*probabilityInsomnia_nightMotion
            insomniaProb = 0.5*insomnia + probabilityInsomnia_nightMotion
            
        else:
            probabilityInsomnia_nightMotion = 0.7*probabilityInsomnia_nightMotion
            insomniaProb = 0.3*insomnia + probabilityInsomnia_nightMotion
                
        line = '\t\"probability(Insomnia|nightMotion)\":'+str(probabilityInsomnia_nightMotion) + ', \n'
        outputFile.writelines(line)    
        line = '\t\"sleepDisordersProbability\":'+str(insomniaProb) + ', \n'
        outputFile.writelines(line)
        
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
                
        line = '\t\"freezing\":{\n' + '\t\t\"result\":' + str(round(percent_freezing*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,freezing_events))+']\n' + '\t},\n'
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
                
        line = '\t\"festination\":{\n' + '\t\t\"result\":' + str(round(percent_festination*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,festination_events))+']\n' + '\t},\n'
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
                
        line = '\t\"fallDown\":{\n' + '\t\t\"result\":' + str(round(percent_fall_down*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,fall_down_events))+']\n' + '\t},\n'
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
        
    
        line = '\t\"lossBalance\":{\n' + '\t\t\"result\":' + str(round(percent_loss_of_balance*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,loss_of_balance_events))+']\n' + '\t},\n'
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
            
        line = '\t\"visitBathroom\":{\n' + '\t\t\"result\":' + str(round(percent_nr_visits_bathroom*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,nr_visits_bathroom))+']\n' + '\t},\n'
        outputFile.writelines(line)
        
        incontinence = self.incontinence
        
        line = '\t\"incontinence\":'+str(incontinence) + ', \n'
        outputFile.writelines(line)

        if(percent_nr_visits_bathroom>=0):            
            probabilityIncontinence_visitsBathroom = 0.7*(percent_nr_visits_bathroom)
        else:
            # for decreasing number of visits to the bathroom the probability of Parkinson events is very low
            probabilityIncontinence_visitsBathroom = 0.001 

        incontinenceProb = 0.3*incontinence + probabilityIncontinence_visitsBathroom           
        
        line = '\t\"probability(Incontinence|visitsBathroom)\":'+str(round(probabilityIncontinence_visitsBathroom,2)) + ', \n'
        outputFile.writelines(line)    
        line = '\t\"incontinenceProbability\":'+str(round(incontinenceProb,2)) + ', \n'
        outputFile.writelines(line)
        
        #plot a graph of the number of visits to the bathroom over the investigated days
        showGraph_bathroom = 0
        if showGraph_bathroom:
            fig = plt.figure()              
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
                
        line = '\t\"digitalTimeSpent\":{\n' + '\t\t\"result\":' + str(round(percent_time_dit*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,time_dit))+']\n' + '\t},\n'
        outputFile.writelines(line)
        
        if(percent_time_dit>=0):            
            probabilityDigitalAddiction_timeDit = 0.6*(percent_time_dit)
            probabilityApathy_timeDit = 0.2*(percent_time_dit)            
        else:
            # for decreasing digital time usage the probability of addiction is very low
            probabilityDigitalAddiction_timeDit = 0.001 
            probabilityApathy_timeDit = 0.001

        probDigitalAddiction = 0.4*self.comorbiditesPsychiatrist + probabilityDigitalAddiction_timeDit

        line = '\t\"probability(digitalAddiction|digitalTimeUsage)\":' + str(round(probabilityDigitalAddiction_timeDit,2)) + ',\n' 
        outputFile.writelines(line)            
        line = '\t\"digitalAddictionProbability\":' + str(round(probDigitalAddiction,2)) + ',\n' 
        outputFile.writelines(line)
        
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
             
        line = '\t\"abnormalDigitalBehaviours\":{\n' + '\t\t\"result\":' + str(round(percent_abnormal_dit*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,nr_abnormal_dit_behaviours))+']\n' + '\t},\n'
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

        cognitiveFunctions = self.cognitiveFunctions
        if(cognitiveFunctions):
            probabilityDigitalConfusion_abnormalDigitalBehaviour = 0.6*probabilityDigitalConfusion_abnormalDigitalBehaviour		
            probDigitalConfusion = probabilityDigitalConfusion_abnormalDigitalBehaviour
        else:
            probabilityDigitalConfusion_abnormalDigitalBehaviour = 0.7*probabilityDigitalConfusion_abnormalDigitalBehaviour		
            probDigitalConfusion =probabilityDigitalConfusion_abnormalDigitalBehaviour + 0.3*(1-int(cognitiveFunctions))
           
        line = '\t\"probability(digitalConfusion|abnormalDigitalBehaviour)\":' + str(round(probabilityDigitalConfusion_abnormalDigitalBehaviour,2)) + ',\n' 
        outputFile.writelines(line)   
        line = '\t\"digitalConfusionProbability\":' + str(round(probDigitalConfusion,2)) + ',\n' 
        outputFile.writelines(line)
        
        probApathy = probabilityApathy_stationary + probabilityApathy_dailyMotion + probabilityApathy_leavingHouse + probabilityApathy_timeDit                      
    
        line = '\t\"probability(Apathy|stationaryBehaviour)\":' + str(round(probabilityApathy_stationary,2)) + ',\n' 
        outputFile.writelines(line)
        
        line = '\t\"probability(Apathy|dailyMotion)\":' + str(round(probabilityApathy_dailyMotion,2)) + ',\n' 
        outputFile.writelines(line)
        
        line = '\t\"probability(Apathy|leavingHouse)\":' + str(round(probabilityApathy_leavingHouse,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(Apathy|digitalTimeUsage)\":' + str(round(probabilityApathy_timeDit,2)) + ',\n' 
        outputFile.writelines(line)

        line = '\t\"apathyProbability\":' + str(round(probApathy,2)) + ',\n' 
        outputFile.writelines(line)
        
        probParkinsonsEvents = probabilityParkinsonsEvents_festination + probabilityParkinsonsEvents_freezing + probabilityParkinsonsEvents_fall_down  + probabilityParkinsonsEvents_lossBalance
        
        line = '\t\"probability(ParkinsonsEvents|freezing)\":' + str(round(probabilityParkinsonsEvents_freezing,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ParkinsonsEvents|festination)\":' + str(round(probabilityParkinsonsEvents_festination,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ParkinsonsEvents|fallDown)\":' + str(round(probabilityParkinsonsEvents_fall_down,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ParkinsonsEvents|lossOfBalance)\":' + str(round(probabilityParkinsonsEvents_lossBalance,2)) + ',\n' 
        outputFile.writelines(line)
    
        line = '\t\"ParkinsonsEventsProbability\":' + str(round(probParkinsonsEvents,2)) + ',\n' 
        outputFile.writelines(line)  

        probImprovedBehaviour = probabilityImprovedBehaviour_abnormalDigitalBehaviour + probabilityImprovedBehaviour_dailyMotion + probabilityImprovedBehaviour_fallDown + probabilityImprovedBehaviour_festination + probabilityImprovedBehaviour_freezing + probabilityImprovedBehaviour_lossBalance + probabilityImprovedBehaviour_nightMotion + probabilityImprovedBehaviour_stationary + probabilityImprovedBehaviour_leavingHouse
        
        if(probImprovedBehaviour>1):
            probImprovedBehaviour = 1
            
        line = '\t\"probability(ImprovedBehaviour|stationary)\":' + str(round(probabilityImprovedBehaviour_stationary,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|dailyMotion)\":' + str(round(probabilityImprovedBehaviour_dailyMotion,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|nightMotion)\":' + str(round(probabilityImprovedBehaviour_nightMotion,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|leavingHouse)\":' + str(round(probabilityImprovedBehaviour_leavingHouse,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|fallDown)\":' + str(round(probabilityImprovedBehaviour_fallDown,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|festination)\":' + str(round(probabilityImprovedBehaviour_festination,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|freezing)\":' + str(round(probabilityImprovedBehaviour_freezing,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|lossOfBalance)\":' + str(round(probabilityImprovedBehaviour_lossBalance,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|abnormalDigitalBehaviour)\":' + str(round(probabilityImprovedBehaviour_abnormalDigitalBehaviour,2)) + ',\n' 
        outputFile.writelines(line)
        
        line = '\t\"ImprovedBehaviourProbability\":' + str(round(probImprovedBehaviour,2)) + ',\n' 
        outputFile.writelines(line)  
        
        line = '}]'
        outputFile.writelines(line)
    
        outputFile.close()  
        
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
        
        line = '\t\"stationaryBehaviour\":{\n' + '\t\t\"result\":' + str(round(percent_stationary*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,stationary))+']\n' + '\t},\n'
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
                
        line = '\t\"dailyMotion\":{\n' + '\t\t\"result\":' + str(round(percent_dailyMotion*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,dailyMotion))+']\n' + '\t},\n'
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
            line = 'Patient leaving the house, increase of: ' + str(round(percent_leavingHouse*100)) + '%; ' + str(nr_leaving_the_house) + "\n"
            
        elif percent_leavingHouse < -0.1:
            line = 'Patient leaving the house, decrease of: ' + str(round(-percent_leavingHouse*100)) + '%; ' + str(nr_leaving_the_house) + "\n"
            
        else:
            line = 'Patient leaving the house, no deviations; ' + str(nr_leaving_the_house) + "\n"
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
    
        line = '\t\"leavingHouse\":{\n' + '\t\t\"result\":' + str(round(percent_leavingHouse*100)) + ',\n' + '\t\t\"events\":[' +','.join(map(str,nr_leaving_the_house))+']\n' + '\t},\n'
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
        
        line = '\t\"nightMotion\":{\n' + '\t\t\"result\":' + str(round(percent_nightMotion*100)) + ',\n' + '\t\t\"events\":[' +','.join(map(str,nr_night_visits))+']\n' + '\t},\n'
        outputFile.writelines(line)
    
        insomnia = self.insomnia
        line = '\t\"insomnia\":'+str(insomnia)+',\n'
        outputFile.writelines(line)
    
        if(percent_nightMotion>=0):
            probabilityInsomnia_nightMotion = percent_nightMotion
            probabilityImprovedBehaviour_nightMotion = 0.001            
        else:
            # for decreasing night motion the probability of insomnia is very low
            probabilityInsomnia_nightMotion = 0.001
            probabilityImprovedBehaviour_nightMotion = -0.2*percent_nightMotion
                      
        if(insomnia):
            probabilityInsomnia_nightMotion = 0.5*probabilityInsomnia_nightMotion
            insomniaProb = 0.5*insomnia + probabilityInsomnia_nightMotion
            
        else:
            probabilityInsomnia_nightMotion = 0.7*probabilityInsomnia_nightMotion
            insomniaProb = 0.3*insomnia + probabilityInsomnia_nightMotion
                
        line = '\t\"probability(Insomnia|nightMotion)\":'+str(probabilityInsomnia_nightMotion) + ', \n'
        outputFile.writelines(line)    
        line = '\t\"sleepDisordersProbability\":'+str(insomniaProb) + ', \n'
        outputFile.writelines(line)
        
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
                
        line = '\t\"abnormalEvents\":{\n' + '\t\t\"result\":' + str(round(percent_abnormalEvents*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,abnormalEvents))+']\n' + '\t},\n'
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
       
        if(comorbiditesPsychiatrist&comorbiditesNeurologist):
            probabilityConfusion_abnormalEvents = 0.5*probabilityConfusion_abnormalEvents
            probConfusion = probabilityConfusion_abnormalEvents + 0.3*comorbiditesNeurologist + 0.3*comorbiditesPsychiatrist
        elif(comorbiditesPsychiatrist):
            probabilityConfusion_abnormalEvents = 0.65*probabilityConfusion_abnormalEvents
            probConfusion = probabilityConfusion_abnormalEvents + 0.35*comorbiditesPsychiatrist
        elif(comorbiditesNeurologist):
            probabilityConfusion_abnormalEvents = 0.65*probabilityConfusion_abnormalEvents
            probConfusion = probabilityConfusion_abnormalEvents + 0.35*comorbiditesNeurologist 
        else:
            probabilityConfusion_abnormalEvents = 0.7*probabilityConfusion_abnormalEvents
            probConfusion = probabilityConfusion_abnormalEvents 
           
        line = '\t\"probability(confusion|abnormalEvents)\":' + str(round(probabilityConfusion_abnormalEvents,2)) + ',\n' 
        outputFile.writelines(line)   
        line = '\t\"confusionProbability\":' + str(round(probConfusion,2)) + ',\n' 
        outputFile.writelines(line)
        
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
                
        line = '\t\"fallDown\":{\n' + '\t\t\"result\":' + str(round(percent_fall_down*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,fall_down_events))+']\n' + '\t},\n'
        outputFile.writelines(line)
        
        if(percent_fall_down>=0):            
            probabilityMovementIssues_fall_down = 0.5*percent_fall_down
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
        
    
        line = '\t\"lossBalance\":{\n' + '\t\t\"result\":' + str(round(percent_loss_of_balance*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,loss_of_balance_events))+']\n' + '\t},\n'
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
            probabilityMovementIssues_lossBalance = 0.5*percent_loss_of_balance
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
            
        line = '\t\"visitBathroom\":{\n' + '\t\t\"result\":' + str(round(percent_nr_visits_bathroom*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,nr_visits_bathroom))+']\n' + '\t},\n'
        outputFile.writelines(line)
        
        incontinence = self.incontinence
        
        line = '\t\"incontinence\":'+str(incontinence) + ', \n'
        outputFile.writelines(line)

        if(percent_nr_visits_bathroom>=0):            
            probabilityIncontinence_visitsBathroom = 0.7*(percent_nr_visits_bathroom)
        else:
            # for decreasing number of visits to the bathroom the probability of Parkinson events is very low
            probabilityIncontinence_visitsBathroom = 0.01 

        incontinenceProb = 0.3*incontinence + probabilityIncontinence_visitsBathroom           
        
        line = '\t\"probability(Incontinence|visitsBathroom)\":'+str(round(probabilityIncontinence_visitsBathroom,2)) + ', \n'
        outputFile.writelines(line)    
        line = '\t\"incontinenceProbability\":'+str(round(incontinenceProb,2)) + ', \n'
        outputFile.writelines(line)
        
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
                
        line = '\t\"digitalTimeSpent\":{\n' + '\t\t\"result\":' + str(round(percent_time_dit*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,time_dit))+']\n' + '\t},\n'
        outputFile.writelines(line)
        
        if(percent_time_dit>=0):            
            probabilityDigitalAddiction_timeDit = 0.6*(percent_time_dit)
            probabilityApathy_timeDit = 0.2*(percent_time_dit)
        else:
            # for decreasing digital time usage the probability of addiction is very low
            probabilityDigitalAddiction_timeDit = 0.01 
            probabilityApathy_timeDit = 0.01

        probDigitalAddiction = 0.4*self.comorbiditesPsychiatrist + probabilityDigitalAddiction_timeDit

        line = '\t\"probability(digitalAddiction|digitalTimeUsage)\":' + str(round(probabilityDigitalAddiction_timeDit,2)) + ',\n' 
        outputFile.writelines(line)            
        line = '\t\"digitalAddictionProbability\":' + str(round(probDigitalAddiction,2)) + ',\n' 
        outputFile.writelines(line)
        
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
             
        line = '\t\"abnormalDigitalBehaviours\":{\n' + '\t\t\"result\":' + str(round(percent_abnormal_dit*100)) + ',\n' + '\t\t\"events\":['+','.join(map(str,nr_abnormal_dit_behaviours))+']\n' + '\t},\n'
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
           
        line = '\t\"probability(digitalConfusion|abnormalDigitalBehaviour)\":' + str(round(probabilityDigitalConfusion_abnormalDigitalBehaviour,2)) + ',\n' 
        outputFile.writelines(line)   
        line = '\t\"digitalConfusionProbability\":' + str(round(probDigitalConfusion,2)) + ',\n' 
        outputFile.writelines(line)
        
        probApathy = probabilityApathy_stationary + probabilityApathy_leavingHouse + probabilityApathy_timeDit+probabilityApathy_dailyMotion                      
    
        line = '\t\"probability(Apathy|stationaryBehaviour)\":' + str(round(probabilityApathy_stationary,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(Apathy|dailyMotion)\":' + str(round(probabilityApathy_dailyMotion,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(Apathy|leavingHouse)\":' + str(round(probabilityApathy_leavingHouse,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(Apathy|digitalTimeUsage)\":' + str(round(probabilityApathy_timeDit,2)) + ',\n' 
        outputFile.writelines(line)

        line = '\t\"apathyProbability\":' + str(round(probApathy,2)) + ',\n' 
        outputFile.writelines(line)
        
        probMovementIssues = probabilityMovementIssues_fall_down  + probabilityMovementIssues_lossBalance + probabilityMovementIssues_leavingHouse + probabilityMovementIssues_stationary + probabilityMovementIssues_dailyMotion
        
        line = '\t\"probability(MovementIssues|fallDown)\":' + str(round(probabilityMovementIssues_fall_down,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(MovementIssues|lossOfBalance)\":' + str(round(probabilityMovementIssues_lossBalance,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(MovementIssues|stationaryBehaviour)\":' + str(round(probabilityMovementIssues_stationary,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(MovementIssues|dailyMotion)\":' + str(round(probabilityMovementIssues_dailyMotion,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(MovementIssues|leavingHouse)\":' + str(round(probabilityMovementIssues_leavingHouse,2)) + ',\n'                        
        outputFile.writelines(line)
        
        line = '\t\"MovementIssuesProbability\":' + str(round(probMovementIssues,2)) + ',\n' 
        outputFile.writelines(line)                
        
        probImprovedBehaviour = probabilityImprovedBehaviour_abnormalDigitalBehaviour + probabilityImprovedBehaviour_dailyMotion + probabilityImprovedBehaviour_fallDown + probabilityImprovedBehaviour_abnormalEvents + probabilityImprovedBehaviour_lossBalance + probabilityImprovedBehaviour_nightMotion + probabilityImprovedBehaviour_stationary + probabilityImprovedBehaviour_leavingHouse
        
        if(probImprovedBehaviour>1):
            probImprovedBehaviour = 1
        
        line = '\t\"probability(ImprovedBehaviour|confusedBehaviours)\":' + str(round(probabilityImprovedBehaviour_abnormalEvents,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|stationary)\":' + str(round(probabilityImprovedBehaviour_stationary,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|dailyMotion)\":' + str(round(probabilityImprovedBehaviour_dailyMotion,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|nightMotion)\":' + str(round(probabilityImprovedBehaviour_nightMotion,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|leavingHouse)\":' + str(round(probabilityImprovedBehaviour_leavingHouse,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|fallDown)\":' + str(round(probabilityImprovedBehaviour_fallDown,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|lossOfBalance)\":' + str(round(probabilityImprovedBehaviour_lossBalance,2)) + ',\n' 
        outputFile.writelines(line)
        line = '\t\"probability(ImprovedBehaviour|abnormalDigitalBehaviour)\":' + str(round(probabilityImprovedBehaviour_abnormalDigitalBehaviour,2)) + ',\n' 
        outputFile.writelines(line)
        
        line = '\t\"ImprovedBehaviourProbability\":' + str(round(probImprovedBehaviour,2)) + ',\n' 
        outputFile.writelines(line)  
        
        line = '\t}\n]'
        outputFile.writelines(line)
    
        outputFile.close()    
        
    def multimodalFusionalgorithms(self,patientId,currentDate):
    
        # define the investigated time interval 
        investigatedPeriodinDays = 10 # analyze the variables over the last n days            
        commentsEnabled = 1
        
        #output file of the MF module containing the results of the analysis          
        outputMFpath = '../output/ehr'
        outputMF_File =  'participantID' + str(patientId) + '_' + str(currentDate) + '_outputResultsMF.txt'              
        outputFileMF = outputMFpath + '/' + outputMF_File   
        outputFile = open(outputFileMF,'w')
       
        # obtain the medical data of the patient with the provided patientId 
        inputEHRpath = '../input/EHR'
        inputEHRFile =  'participantID' + str(patientId) + '_EHR.txt'              
        inputEHRFileMF =inputEHRpath + '/' + inputEHRFile  
                              
        main_diagnosis, disease_level, age, gender, civilStatus, bmi, active, mobility, gradeDependence, autonomousWalk, independenceDailyActivities, comorbiditesNeurologist, comorbiditesPsychiatrist, cognitiveFunctions, comorbiditesCardiovascular, hipertension, comorbiditesUrinary, incontinence, insomnia  = self.parseEHRFile(inputEHRFileMF)
        
        self.mainDiagnose = main_diagnosis # the main diagnose is 1 for Parkinson's and 0 for Alzheimer's 
        self.disease_level = disease_level
        self.insomnia = insomnia
        self.incontinence = incontinence
        self.comorbiditesNeurologist = comorbiditesNeurologist
        self.comorbiditesUrinary= comorbiditesUrinary
        self.comorbiditesPsychiatrist= comorbiditesPsychiatrist
        self.cognitiveFunctions = cognitiveFunctions
        
        if self.mainDiagnose==1:
            str_patient = 'The patient has Parkinsons level ' + str(self.disease_level)  
            if commentsEnabled: 
                print str_patient
        else:
            str_patient = 'The patient has Alzheimers level ' + str(self.disease_level)  
            if commentsEnabled: 
                print str_patient
                
        #currentDay = currentDate.day
        startDate = currentDate + timedelta(days= -investigatedPeriodinDays)
        if commentsEnabled: 
            print startDate
    
        line = '[\n\t{\n'+'\t\"patientID\":\"patient'+str(patientId)+ '\",\n'
        outputFile.writelines(line)
    
        line = '\t\"startDate\":\"' + str(startDate) + '\",\n' 
        outputFile.writelines(line)
        line = '\t\"endDate\":\"' + str(currentDate) + '\",\n' 
        outputFile.writelines(line)
     
        #downloadFileFromCloud.downloadFile_Cloud(inputEHRPath,inputEHRFileMF) 
     
        # call the digital abnormal behaviour module for finding the number of abnormal events and the total interaction time
        inputDITpath = '../input/DIT'
        
        ## current implementation of the DIT
        inputDITFiletoMF = inputDITpath + '/' + 'inputDITfile.txt'
        date_from = str(startDate) 
        date_to = str(currentDate) 
        response = getDIT.get_dataABD(date_from, date_to, inputDITFiletoMF)
        if response>0:
            abnormalUsageTime, nrAbnormalEvents, type_events_T, type_events_S, type_events_ST = self.parseDITFile_allEvents(inputDITFiletoMF)
            print "Dit parsed"
        else:
            print "No file received in DIT"                
                
        # extract the ABD parameters for each of the investigated day in the predefined period
        stationary = np.zeros(shape= (investigatedPeriodinDays))
        dailyMotion = np.zeros(shape= (investigatedPeriodinDays))
        nr_visits_bathroom = np.zeros(shape= (investigatedPeriodinDays))
        nr_leaving_the_house = np.zeros(shape= (investigatedPeriodinDays))
    
        freezing_events = np.zeros(shape= (investigatedPeriodinDays))
        festination_events = np.zeros(shape= (investigatedPeriodinDays))
        loss_of_balance_events = np.zeros(shape= (investigatedPeriodinDays))
        fall_down_events = np.zeros(shape= (investigatedPeriodinDays))
        #movement_evolution_events = np.zeros(shape= (investigatedPeriodinDays))
        nr_night_visits = np.zeros(shape= (investigatedPeriodinDays))
        # parameters for DIT analysis
        time_dit = np.zeros(shape= (investigatedPeriodinDays))
        abnormalEvents = np.zeros(shape= (investigatedPeriodinDays))
        nr_abnormalBehaviours_attachment = np.zeros(shape= (investigatedPeriodinDays))
        nr_abnormalBehaviours_medication = np.zeros(shape= (investigatedPeriodinDays))
        nr_abnormalBehaviours_appointment = np.zeros(shape= (investigatedPeriodinDays))
                
        inputPath = '../input'                      
        for i in range(0,investigatedPeriodinDays):    
            #print i
            currentdate = startDate + timedelta(days= +i)
            str_date = currentdate.strftime('%d-%m-%Y')
            
            # files will be loaded from the input folder, while the results will be stored in the output folder          
            inputABDFileMF = 'participantID' + str(patientId) + '_' + str_date + '.txt'              
            inputABDFilePath =  inputPath + '/ABD' + '/' + inputABDFileMF  
            
            #downloadFileFromCloud.downloadFile_Cloud(inputABDFilePath,inputFileMF)    
            #print inputABDFilePath
            
            if (os.path.isfile(inputABDFilePath)):                    
                station, dailyMov, freezing_nr, festination_nr, loss_of_balance_nr, fall_down_nr, nr_visits_bath, nr_leaving_house, nr_night_visit, confusion_nr = self.parseABDFile(inputABDFilePath)                                       
            else:    
                station = 0
                dailyMov = 0
                nr_visits_bath = 0
                festination_nr = 0
                freezing_nr = 0
                fall_down_nr = 0
                loss_of_balance_nr = 0
                nr_leaving_house = 0                    
                nr_night_visit = 0
                confusion_nr = 0
                print 'File ' + inputABDFilePath + ' not found.\n'              
            
            stationary[i] = station
            abnormalEvents[i] = confusion_nr
            dailyMotion[i] = round(dailyMov,2)
            nr_visits_bathroom[i] = nr_visits_bath
            festination_events[i] = festination_nr
            freezing_events[i] = freezing_nr
            fall_down_events[i] = fall_down_nr
            loss_of_balance_events[i] = loss_of_balance_nr
            nr_leaving_the_house[i] = nr_leaving_house                    
            nr_night_visits[i] = nr_night_visit
            
            inputDITFiletoMF = inputDITpath + '/' + 'participantID' + str(patientId) + '_' + str_date + '.txt'   
            if (os.path.isfile(inputDITFiletoMF)):
                time_dit[i], nr_abnormalBehaviours_attachment[i], nr_abnormalBehaviours_medication[i], nr_abnormalBehaviours_appointment[i]  = self.parseDITFile(inputDITFiletoMF)                                    
            else:
                time_dit[i] = 0
                nr_abnormalBehaviours_attachment[i] = 0
                nr_abnormalBehaviours_medication[i] = 0
                nr_abnormalBehaviours_appointment[i] = 0
                print 'File ' + inputDITFiletoMF + ' not found.\n'       
               
        #assess the stationary behaviour and leaving the house events for detecting signs of apathy     
        nr_abnormal_dit_behaviours = nr_abnormalBehaviours_attachment + nr_abnormalBehaviours_medication + nr_abnormalBehaviours_appointment
                
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
        
        #Different sets of functionalities are evaluated in the case of Parkinson's or Alzheimer's disease
        if (self.mainDiagnose==1):
            self.evaluateParkinsonsActivities(outputFile,investigatedPeriodinDays)
        else:
            self.evaluateAlzheimersActivities(outputFile,investigatedPeriodinDays)                   
              
        # upload the output file to the cloud containing the analysis results
        uploadResults = 0
        if(uploadResults):
        
            outputPath= '../output'        
            outFilePath =  outputPath + '/ehr' + '/' + outputMF_File
            uploadFileToCloud.uploadFile_Cloud(outFilePath,outputMF_File)
    
        print('Multimodal Fusion module completed.')       
    
if __name__ == '__main__':
    
    # define the set of parameters
    patientId = 2      
    currentDate = datetime.date.today() # the MF module will be called using the current date   
    str_date = currentDate.strftime('%d-%m-%Y')        
    currentDate = currentDate.replace(2017,5,12) #this date is used for testing purposes

    mf=MultimodalFusion()
    mf.multimodalFusionalgorithms(patientId,currentDate)
    
