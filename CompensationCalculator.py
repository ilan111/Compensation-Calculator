# -*- coding: utf-8 -*-
"""
Created on Sun May 10 12:38:07 2020

@author: ilan-
Calculator for calculating comitment values for active workers
Team members: Ilan Yadgarov, Aviv Perets, Zohar Azriev
"""

import xlrd
import datetime
import math
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

#####################################
#get all information from excel files to list of lists by the sheet number:
#####################################

file_location=r"data5.xlsx"
workbook = xlrd.open_workbook(file_location)
data_sheet = workbook.sheet_by_index(0)
sheet2 = workbook.sheet_by_index(1)
sheet3_MenValues=workbook.sheet_by_index(2)
sheet4_WomenValues=workbook.sheet_by_index(3)

#All data of sheets in a list of lists
database=[[data_sheet.cell_value(r,c) for c in range(data_sheet.ncols)] 
        for r in range(data_sheet.nrows)]

data2=[[sheet2.cell_value(r,c) for c in range(sheet2.ncols)] 
        for r in range(sheet2.nrows)]

MenValues=[[sheet3_MenValues.cell_value(r,c) for c in range(sheet3_MenValues.ncols)] 
        for r in range(sheet3_MenValues.nrows)]

WomenValues=[[sheet4_WomenValues.cell_value(r,c) for c in range(sheet4_WomenValues.ncols)] 
        for r in range(sheet4_WomenValues.nrows)]

rows_database=len(database)
#####################################
#Methos to return specific values:
#####################################

def getWorkerID(rowNumber):
    return int(database[rowNumber][0])

#HIVUN
def getDiscountRate(year):
    rows_data2=len(data2)
    for i in range(rows_data2):
        if year==data2[i][0]:
            return float(data2[i][1])
        
def getSeif14_Rate(ID):
    rows_database=len(database)
    for i in range(rows_database):
        if database[i][0]==ID:
            if database[i][8]!='':
                return int(database[i][8])
    return 0

def HasSeif14(ID):
    rows_database=len(database)
    for i in range(rows_database):
        if database[i][0]==ID and (database[i][8]!=''):
                return True
    return False

def getPeriod_Without_Seif14(ID):
    rows_database=len(database)
    for i in range(rows_database):
       if(database[i][0]==ID and (database[i][7]!='')):
            GotSeif14DateXL=database[i][7]
            HiredDateXL=database[i][5]
            GotSeif14Date=xlrd.xldate_as_datetime(GotSeif14DateXL,0)
            HiredDate=xlrd.xldate_as_datetime(HiredDateXL,0)
            Period = GotSeif14Date.year - HiredDate.year -((GotSeif14Date.month, GotSeif14Date.day) < (HiredDate.month, HiredDate.day))  
            return Period
    
def getGender(ID):
    rows_database=len(database)
    for i in range(rows_database):
        if database[i][0]==ID:
            return database[i][3]
        
def getPropertyValue(ID):
    rows_database=len(database)
    for i in range(rows_database):
        if database[i][0]==ID:
            return int(database[i][9])

def getDiposits(ID):
    rows_database=len(database)
    for i in range(rows_database):
        if database[i][0]==ID:
            return int(database[i][10])

def getPaymentFromProperty(ID):
    rows_database=len(database)
    for i in range(rows_database):
        if database[i][0]==ID:
            return int(database[i][12])
        
def getCompletionByCheck(ID):
    rows_database=len(database)
    for i in range(rows_database):
        if database[i][0]==ID and database[i][13]!='':
            return int(database[i][13])
        else: return 0
        
def isActiveWorker(ID):
    rows_database=len(database)
    for i in range(rows_database):
        if database[i][0]==ID and (database[i][11]=='-' or database[i][11]==''):
            return True
    return False

def getSeniority(ID):
    rows_database=len(database)
    for i in range(rows_database):
        if database[i][0]==ID:
            if database[i][11]=='' or database[i][11]=='-'or database[i][11]==None:
                   today = date.today()
                   BeganWorkingDateXL=database[i][5]
                   BeganWorkingDate=xlrd.xldate_as_datetime(BeganWorkingDateXL,0)
                   seniority_in_years = relativedelta(today, BeganWorkingDate).years
                   return int(seniority_in_years) 
            else:
                   LeavingDateXL = database[i][11]
                   BeganWorkingDateXL=database[i][5]
                   LeavingDate=xlrd.xldate_as_datetime(LeavingDateXL,0)
                   BeganWorkingDate=xlrd.xldate_as_datetime(BeganWorkingDateXL,0)
                   seniority_in_years = relativedelta(LeavingDate, BeganWorkingDate).years
                   return int(seniority_in_years)
#print(getSeniority(5))

def getLastSalary(ID):
    rows_database=len(database)
    for i in range(rows_database):
        if(database[i][0]==ID):
            return int(database[i][6])


def getSalaryGrowthRate():
    return int(data2[4][9])


def getRetireAge(gender):
    if gender =='M':
        return 67
    elif gender =='F':
        return 64

#return the q(x+t+1) value
def get_Qxt1(t,age,gender):
    maxAge=age+t+1
    rows_Men=len(MenValues)
    rows_Women=len(WomenValues)
    if gender =='M':
        for i in range (rows_Men):
            if MenValues[i][1]==maxAge:
                return float(MenValues[i][5])
            
    elif gender =='F':
        for i in range (rows_Women):
            if WomenValues[i][1]==maxAge:
                return float(WomenValues[i][5])
            
def get_tPx(t,age,gender):
    maxAge=age+t
    lxPlusT=''
    lx=''
    rows_Men=len(MenValues)
    rows_Women=len(WomenValues)
    if gender =='M':
        for i in range (rows_Men):
            if MenValues[i][1]==age:
                lx=float(MenValues[i][2])
            if MenValues[i][1]==maxAge:
                lxPlusT=float(MenValues[i][2])
                return lxPlusT/lx

    elif gender =='F':
         for i in range (rows_Women):
            if WomenValues[i][1]==age:
                lx=float(WomenValues[i][2])
            if WomenValues[i][1]==maxAge:
                lxPlusT=float(WomenValues[i][2])
                return lxPlusT/lx     
          
def HasProperty(ID):
    rows_database=len(database)
    for i in range(rows_database):
        if(database[i][0]==ID and database[i][9]>0):
            return True
    return False

def getPropertyValue(ID):
    rows_database=len(database)
    for i in range(rows_database):
        if(database[i][0]==ID and database[i][9]>0):
            return int(database[i][9])
    return 0

def getLeavingProp(age):
    Fired=''
    Resigned=''
    if(age>=18 and age<=29):
        Fired=data2[4][5]
        Resigned=data2[4][6]
        return [Fired,Resigned]
    
    elif(age>=30 and age<=39):
        Fired=data2[5][5]
        Resigned=data2[5][6]
        return [Fired,Resigned]
    
    elif(age>=40 and age<=49):
        Fired=data2[6][5]
        Resigned=data2[6][6]
        return [Fired,Resigned]
    
    elif(age>=50 and age<=59):
        Fired=data2[7][5]
        Resigned=data2[7][6]
        return [Fired,Resigned]
    
    elif(age>=60 and age<=67):
        Fired=data2[8][5]
        Resigned=data2[8][6]
        return [Fired,Resigned]
    
#returns the age of the worker
def getWorkerAge(ID):
    rows_database=len(database)
    for i in range(rows_database):
       if(database[i][0]==ID):
            birthDateXL=database[i][4]
            birthDate=xlrd.xldate_as_datetime(birthDateXL,0)
            today = date.today() 
            age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day)) 
  
    return age 

def getSeniorityInMonths(ID):
    rows_database=len(database)
    for i in range(rows_database):
        if database[i][0]==ID:
            if database[i][11]=='' or database[i][11]=='-'or database[i][11]==None:
                   today = date.today()
                   BeganWorkingDateXL=database[i][5]
                   BeganWorkingDate=xlrd.xldate_as_datetime(BeganWorkingDateXL,0)
                   num_months = (today.year - BeganWorkingDate.year) * 12 + (today.month - BeganWorkingDate.month)
                   return int(num_months) 
                   
            else:
                   LeavingDateXL = database[i][11]
                   BeganWorkingDateXL=database[i][5]
                   LeavingDate=xlrd.xldate_as_datetime(LeavingDateXL,0)
                   BeganWorkingDate=xlrd.xldate_as_datetime(BeganWorkingDateXL,0)
                   num_months = (LeavingDate.year - BeganWorkingDate.year) * 12 + (LeavingDate.month - BeganWorkingDate.month)
                   return int(num_months) 

def getDeposits(ID):
    rows_database=len(database)
    for i in range(rows_database):
       if(database[i][0]==ID):
           return database[i][10]

def getPayentFromProperty(ID):
    rows_database=len(database)
    for i in range(rows_database):
       if(database[i][0]==ID):
           return database[i][12]
       
def getCheckAddition(ID):
    rows_database=len(database)
    for i in range(rows_database):
       if(database[i][0]==ID):
           if (database[i][13]==''):
               return 0
           else:    
               return database[i][13]
       
def getAgeOfBeginingWork(ID):
    currentAge=getWorkerAge(ID)
    for i in range(rows_database):
        if database[i][0]==ID:
                   BeganWorkingDateXL=database[i][5]
                   BDayXL=database[i][4]
                   BDay=xlrd.xldate_as_datetime(BDayXL,0)
                   BeganWorkingDate=xlrd.xldate_as_datetime(BeganWorkingDateXL,0)
                   StartedWorkingAge = relativedelta(BeganWorkingDate,BDay).years
                   return StartedWorkingAge

#print("Age Started work: ", getAgeOfBeginingWork(46), "Sen: ", getSeniority(46))

#####################################
#Part 2
#####################################
               
          ############ התחייבות ############

# פקטור אקטוארי
def Factor(ID, CommitmentValue):
    LastSalary=getLastSalary(ID)
    Seniority=getSeniority(ID)
    if(Seniority==0):
        Seniority=getSeniorityInMonths(ID)/12
    Seif14=getSeif14_Rate(ID)
    if(Seif14==0):
        Seif14=1
    return int(CommitmentValue)/(LastSalary*Seniority*1)
    
  # עלות שירות שוטף
def AlutSherutShotef(ID,ComitmentValue):
    Seniority=getSeniority(ID)
    if(Seniority>0):
        return 0
    
    elif(Seniority==0):
        Salary=getLastSalary(ID)
        WorkedPartOfYear=getSeniorityInMonths(ID)/12
        Factor=Factor(ID,ComitmentValue)
        Seif14=getSeif14_Rate(ID)
        if(Seif14==0):
            Seif14=1
        return Salary*WorkedPartOfYear*Factor*Seif14
        
     
# תוחלת שירות
def ServiceExpectation(ID):
    Gender=getGender(ID)
    CurrentAge=getWorkerAge(ID)
    RetirementAge=getRetireAge(Gender)
    tPx=''
    Sum=0
    for t in range(1,RetirementAge-CurrentAge):
        tPx=get_tPx(t,CurrentAge,Gender)
        Sum+=(tPx**t)
    return Sum

#עלות היוון
def CapitalizationCost(OpeningBalance, CapitalizationRate, AlutSherutShotef, Benefits):
    return OpeningBalance*CapitalizationRate+(AlutSherutShotef-Benefits)*(CapitalizationRate/2)
    
#סך ההטבות ששולמו
def SumPaidBenefits(ID):
    propertyPaid=getPayentFromProperty(ID)
    checkAdd=getCheckAddition(ID)
    return int(propertyPaid+checkAdd)

# רווחים / הפסדים אקטואריים
def ProfitsLooses_Commitment(CommitmentOpening, CommitmentClosure, AlutSherutShotef, Hivun, Benefits):
    return CommitmentOpening-CommitmentClosure-AlutSherutShotef-Hivun+Benefits


############ נכסים ############
#הפקדות לנכסי התכנית
def WorkerDeposits(ID):
    Sum=0
    for i in range(2,rows_database):
        if(database[i][0]==ID):
           return database[i][10]
   

#הטבות ששולמו מנכסי התוכנית לכל העובדים שעזבו
def ActiveWorkerBenefits(ID):
    for i in range(2,rows_database):
        if(database[i][0]==ID):
            if isActiveWorker(ID)==False:
                return database[i][12]
    return 0

# שווי נכסי התוכנית יתרת סגירה
def PropertyClosureBalance(ID):
    for i in range(2,rows_database):
        if(database[i][0]==ID):
            return database[i][9]

# תשואה צפויה על נכסי התוכנית
def PropertyYield(OpeningBalance, ExpectedYield, WorkerDeposits,ActiveWorkerBenefits):
    return OpeningBalance*ExpectedYield+(WorkerDeposits-ActiveWorkerBenefits)*(ExpectedYield/2)
        #ExpectedYield= Alut Hivun
        
        
# רווחים / הפסדים אקטואריים
def ProfitsLooses_Property(ClosureBalance, OpeningBalance, ExpectedYield, WorkerDeposits,ActiveWorkerBenefits):
    ClosureBalance-OpeningBalance-ExpectedYield-WorkerDeposits+ActiveWorkerBenefits
    

#####################################
#A function that returns a commitment value by the workes ID:
#####################################
    
# calculates the commitment value
def Calculate_Commitment(ID):
    LastSalary=getLastSalary(ID)
    Seniority=getSeniority(ID)
    SalaryGrowthRate=getSalaryGrowthRate()
    Gender=getGender(ID)
    RetirementAge=getRetireAge(Gender)
    CurrentAge=getWorkerAge(ID)
    StartedWorkingAge=getAgeOfBeginingWork(ID)
    Period_Without_Seif14=getPeriod_Without_Seif14(ID)    
    if(Period_Without_Seif14==None):
        Period_Without_Seif14=Seniority
    Period_With_Seif14=Seniority-Period_Without_Seif14
    Property=0
    if(HasProperty(ID)):
        Property=getPropertyValue(ID)
    Seif14_Rate=getSeif14_Rate(ID)
    Sum=0
    Numerator=0
    Denominator=0
    tPx=''
    Qxt1=''
    if CurrentAge<RetirementAge:
        if((Period_Without_Seif14==None or Period_Without_Seif14==0) and Seif14_Rate==100):
            Sum=0
            return Sum
                
        elif(HasSeif14(ID)):
            #if had seif 14 from first day
            if(Period_With_Seif14==Seniority):
                #complement of seif 14 in precentage
                Seif14_Rate=(100-Seif14_Rate)/100
                Period_With_Seif14=Seniority-Period_Without_Seif14
                for t in range(RetirementAge-CurrentAge):
                    #if t!=0:
                    tPx=get_tPx(t,CurrentAge,Gender)
                    Qxt1=get_Qxt1(t,CurrentAge,Gender)
                    ChanceToGetFired=getLeavingProp(CurrentAge+t)[0]
                    ChanceToGetRetired=getLeavingProp(CurrentAge+t)[1]
                    #in case of death:
                    Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*Qxt1
                    Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                    Sum+=(LastSalary*Seniority*Seif14_Rate*(Numerator/Denominator))
                    #in case of dismissal:
                    Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*ChanceToGetFired
                    Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                    Sum+=(LastSalary*Seniority*Seif14_Rate*(Numerator/Denominator))
                    #property calculation in case of retirement:
                    PropertySum=Property*Seif14_Rate*(tPx**t)*ChanceToGetRetired
                    Sum+=PropertySum       
                return Sum
            
            elif(Period_With_Seif14<Seniority and Period_With_Seif14>=0):
                for t in range(RetirementAge-CurrentAge):
                    #if t!=0:
                    tPx=get_tPx(t,CurrentAge,Gender)
                    Qxt1=get_Qxt1(t,CurrentAge,Gender)
                    ChanceToGetFired=getLeavingProp(CurrentAge+t)[0]
                    ChanceToGetRetired=getLeavingProp(CurrentAge+t)[1]
                    #in case of death:
                    Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*Qxt1
                    Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                    Sum+=(LastSalary*Period_Without_Seif14*(Numerator/Denominator))
                    #in case of dismissal:
                    Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*ChanceToGetFired
                    Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                    Sum+=(LastSalary*Period_Without_Seif14*(Numerator/Denominator))
                    #property calculation in case of retirement:
                    PropertySum=Property*(tPx**t)*ChanceToGetRetired
                    Sum+=PropertySum   
                    #complement of seif 14 in precentage
                    Seif14_Rate=(100-Seif14_Rate)/100
                    Period_With_Seif14=Seniority-Period_Without_Seif14
                for t in range(RetirementAge-CurrentAge):
                    #if t!=0:
                    tPx=get_tPx(t,CurrentAge,Gender)
                    Qxt1=get_Qxt1(t,CurrentAge,Gender)
                    ChanceToGetFired=getLeavingProp(CurrentAge+t)[0]
                    ChanceToGetRetired=getLeavingProp(CurrentAge+t)[1]
                    #in case of death:
                    Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*Qxt1
                    Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                    Sum+=(LastSalary*Period_With_Seif14*Seif14_Rate*(Numerator/Denominator))
                   #in case of dismissal:
                    Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*ChanceToGetFired
                    Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                    Sum+=(LastSalary*Period_With_Seif14*Seif14_Rate*(Numerator/Denominator))
                    #property calculation in case of retirement:
                    PropertySum=Property*Seif14_Rate*(tPx**t)*ChanceToGetRetired
                    Sum+=PropertySum   
                return Sum
            
        else:
            for t in range(RetirementAge-CurrentAge):
                #if t!=0:
                tPx=get_tPx(t,CurrentAge,Gender)
                Qxt1=get_Qxt1(t,CurrentAge,Gender)
                ChanceToGetFired=getLeavingProp(CurrentAge+t)[0]
                ChanceToGetRetired=getLeavingProp(CurrentAge+t)[1]
                #in case of death:
                Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*Qxt1
                Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                Sum+=(LastSalary*Seniority*(Numerator/Denominator))
               #in case of dismissal:
                Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*ChanceToGetFired
                Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                Sum+=(LastSalary*Seniority*(Numerator/Denominator))
               #property calculation in case of retirement:
                PropertySum=Property*(tPx**t)*ChanceToGetRetired
                Sum+=PropertySum
            return Sum
        
    else:
        return (CurrentAge-RetirementAge)*LastSalary
#print(getSeniorityInMonths(20))
#print(getAlutSherutShotef(20,Calculate_Commitment(20)))
        

#####################################
#A function that calculates commitment only for active workers and prints the results:
#####################################
        
def CalculateForActiveWorkers():
    rows_database=len(database)
    WorkerID=None
    Value=''
    TotalSum=0
    #print("ID          Value")
    for i in range (2,rows_database):
    #i=2
    
    #while(i<rows_database):
            
        WorkerID=((getWorkerID(i)))
        if isActiveWorker(WorkerID)==True:
            Value=Calculate_Commitment(WorkerID)
            TotalSum+=Value
            #print(WorkerID,"        ",Value)
        i=i+1
    #print("Total        ",TotalSum)
    return TotalSum

#call for a function that displays all active workers with their comitment values
#CalculateForActiveWorkers()



    
#print(getFactor(3,int(Calculate_Commitment(3))))
   
def Calculate_Commitment_check(ID):
    LastSalary=getLastSalary(ID)
    Seniority=getSeniority(ID)
    SalaryGrowthRate=getSalaryGrowthRate()
    Gender=getGender(ID)
    RetirementAge=getRetireAge(Gender)
    CurrentAge=getWorkerAge(ID)
    StartedWorkingAge=getAgeOfBeginingWork(ID)
    Period_Without_Seif14=getPeriod_Without_Seif14(ID)    
    if(Period_Without_Seif14==None):
        Period_Without_Seif14=Seniority
    Period_With_Seif14=Seniority-Period_Without_Seif14
    Property=0
    if(HasProperty(ID)):
        Property=getPropertyValue(ID)
    Seif14_Rate=getSeif14_Rate(ID)
    Sum=0
    Numerator=0
    Denominator=0
    tPx=''
    Qxt1=''
    if CurrentAge<RetirementAge:
        if((Period_Without_Seif14==None or Period_Without_Seif14==0) and Seif14_Rate==100):
            Sum=0
            return Sum
                
        elif(HasSeif14(ID)):
            #if had seif 14 from first day
            if(Period_With_Seif14==Seniority):
                #complement of seif 14 in precentage
                Seif14_Rate=(100-Seif14_Rate)/100
                Period_With_Seif14=Seniority-Period_Without_Seif14
                for t in range(RetirementAge-CurrentAge+1):
                    #if t!=0:

                    
                    tPx=get_tPx(t,CurrentAge,Gender)
                    Qxt1=get_Qxt1(t,CurrentAge,Gender)
                    ChanceToGetFired=getLeavingProp(CurrentAge+t)[0]
                    ChanceToGetRetired=getLeavingProp(CurrentAge+t)[1]
                    #in case of death:
                    Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*Qxt1
                    Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                    Sum+=(LastSalary*Seniority*Seif14_Rate*(Numerator/Denominator))
                    #in case of dismissal:
                    Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*ChanceToGetFired
                    Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                    Sum+=(LastSalary*Seniority*Seif14_Rate*(Numerator/Denominator))
                    #property calculation in case of retirement:
                    PropertySum=Property*Seif14_Rate*(tPx**t)*ChanceToGetRetired
                    Sum+=PropertySum   
                    print("t=",t)
                    print("tPx=",tPx)
                    print("Q(x+t+1)=",Qxt1)
                    print("Chance to be fired=",ChanceToGetFired)
                    print("Chance to be retired", ChanceToGetRetired)
                    print("Current sum=",Sum)
                    print("----------------------")
                return Sum
            
            elif(Period_With_Seif14<Seniority and Period_With_Seif14>=0):
                x=''
                for t in range(Period_Without_Seif14+1):
                    #if t!=0:
                    x=t
                    tPx=get_tPx(t,CurrentAge,Gender)
                    Qxt1=get_Qxt1(t,CurrentAge,Gender)
                    ChanceToGetFired=getLeavingProp(CurrentAge+t)[0]
                    ChanceToGetRetired=getLeavingProp(CurrentAge+t)[1]
                    #in case of death:
                    Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*Qxt1
                    Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                    Sum+=(LastSalary*Period_Without_Seif14*(Numerator/Denominator))
                    #in case of dismissal:
                    Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*ChanceToGetFired
                    Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                    Sum+=(LastSalary*Period_Without_Seif14*(Numerator/Denominator))
                    #property calculation in case of retirement:
                    PropertySum=Property*(tPx**t)*ChanceToGetRetired
                    Sum+=PropertySum   
                    #complement of seif 14 in precentage
                    Seif14_Rate=(100-Seif14_Rate)/100
                    Period_With_Seif14=Seniority-Period_Without_Seif14
                    print("t=",t)
                    print("tPx=",tPx)
                    print("Q(x+t+1)=",Qxt1)
                    print("Chance to be fired=",ChanceToGetFired)
                    print("Chance to be retired", ChanceToGetRetired)
                    print("Current sum=",Sum)
                    print("----------------------")
                for t in range(x+1,RetirementAge-CurrentAge+1):
                    #if t!=0:
                    tPx=get_tPx(t,CurrentAge,Gender)
                    Qxt1=get_Qxt1(t,CurrentAge,Gender)
                    ChanceToGetFired=getLeavingProp(CurrentAge+t)[0]
                    ChanceToGetRetired=getLeavingProp(CurrentAge+t)[1]
                    #in case of death:
                    Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*Qxt1
                    Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                    Sum+=(LastSalary*Period_With_Seif14*Seif14_Rate*(Numerator/Denominator))
                   #in case of dismissal:
                    Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*ChanceToGetFired
                    Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                    Sum+=(LastSalary*Period_With_Seif14*Seif14_Rate*(Numerator/Denominator))
                    #property calculation in case of retirement:
                    PropertySum=Property*Seif14_Rate*(tPx**t)*ChanceToGetRetired
                    Sum+=PropertySum  
                    print("t=",t)
                    print("tPx=",tPx)
                    print("Q(x+t+1)=",Qxt1)
                    print("Chance to be fired=",ChanceToGetFired)
                    print("Chance to be retired", ChanceToGetRetired)
                    print("Current sum=",Sum)
                    print("----------------------")
                return Sum
            
        else:
            x=''
            print(Seniority)
            for t in range(Seniority):
                #if t!=0:
                x=t
                tPx=get_tPx(t,StartedWorkingAge,Gender)
                Qxt1=get_Qxt1(t,StartedWorkingAge,Gender)
                ChanceToGetFired=getLeavingProp(StartedWorkingAge+t)[0]
                ChanceToGetRetired=getLeavingProp(StartedWorkingAge+t)[1]
                #in case of death:
                Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*Qxt1
                Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                Sum+=(LastSalary*Seniority*(Numerator/Denominator))
               #in case of dismissal:
                Numerator=((1+SalaryGrowthRate)**(t+0.5))*((tPx)**t)*ChanceToGetFired
                Denominator=(1+getDiscountRate(t+1)**(t+0.5))
                Sum+=(LastSalary*Seniority*(Numerator/Denominator))
               #property calculation in case of retirement:
                PropertySum=Property*(tPx**t)*ChanceToGetRetired
                Sum+=PropertySum 
                print("t=",t)
                print("tPx in=",tPx)
                print("Q(x+t+1)=",Qxt1)
                print("Chance to be fired=",ChanceToGetFired)
                print("Chance to be retired", ChanceToGetRetired)
                print("Current sum=",Sum)
                print("----------------------")
                if(CurrentAge+t==RetirementAge):
                    break
            for t in range (x+1,CurrentAge-RetirementAge):
                i=1
                Sum+= LastSalary*i
                i=i+1
                print("t=",t)
                print("tPx=",tPx)
                print("Q(x+t+1)=",Qxt1)
                print("Chance to be fired=",ChanceToGetFired)
                print("Chance to be retired", ChanceToGetRetired)
                print("Current sum=",Sum)
                print("----------------------")
            return Sum
        
    else:
        return (CurrentAge-RetirementAge)*LastSalary 

def main():
    
    #נכסים
    sumWorkersDeposits=AllWorkersDeposits()
    sumWorkersPayedBenefits=AllActiveWorkersBenefits()
    sumPropertyClosureBalance=PropertyClosureBalance()
    
    #Calculate_Commitment_check(4)
main()
    
    
    