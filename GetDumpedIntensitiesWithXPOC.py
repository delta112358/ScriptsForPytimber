import pytimber
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
ldb = pytimber.LoggingDB()
import matplotlib.pyplot as plt
import pdb

def getData(startTime,endTime,intensityVariableName,energyVariableName):

    dumpTimes=[]
    dumpedIntensities=[]
    energyTimes=[]
    energiesPP=[]

    timeIntervals = makeTimeIntervals(startTime,endTime)

    for index,timeInterval in enumerate(timeIntervals):
        print(str(index+1)+'. interval')
        print('from '+timeInterval[0].strftime("%Y-%m-%d") +' to '+timeInterval[1].strftime("%Y-%m-%d"))
        print('get intensities ...')
        dumpTimesTemp , dumpedIntensitiesTemp = getVariable(intensityVariableName,timeInterval[0],timeInterval[1])
        print('get energies ...')
        energyTimesTemp,energiesPPTemp = getEnergiesAtDump(energyVariableName,startTime,endTime, dumpTimesTemp)
        print('put data together ...\n')
        dumpTimes=dumpTimes+list(dumpTimesTemp)
        energyTimes=energyTimes+list(energyTimesTemp)
        dumpedIntensities=dumpedIntensities+list(dumpedIntensitiesTemp)
        energiesPP=energiesPP+list(energiesPPTemp)

    return dumpTimes,dumpedIntensities,energyTimes,energiesPP

def makeTimeIntervals(startTime,endTime):

    startTimeLS1= "2013-02-14 00:00:00.000"
    endTimeLS1="2015-04-01 00:00:00.000"

    if startTime >= startTimeLS1 and startTime <= endTimeLS1:
        startTime=endTimeLS1
    if endTime >= startTimeLS1 and endTime <= endTimeLS1:
        endTime=startTimeLS1
    if startTime==endTimeLS1 and endTime==startTimeLS1:
        print ('Interval is in LS1.')
        exit()

    if startTime < startTimeLS1 and endTime > endTimeLS1:
        timeIntervalsBeforeLS1 = makeTimeIntervalList(makeTimeList(startTime,startTimeLS1))
        timeIntervalsAfterLS1 = makeTimeIntervalList(makeTimeList(endTimeLS1,endTime))
        timeIntervals= timeIntervalsBeforeLS1 + timeIntervalsAfterLS1

    else:
        timeIntervals=makeTimeIntervalList(makeTimeList(startTime,endTime))

    return timeIntervals


def makeTimeList(startTime,endTime):
    startTime=datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S.%f")
    endTime=datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S.%f")
    timeIntervals=[startTime]
    previousTime=startTime
    while True:
        newTime=previousTime+relativedelta(months=6)
        if newTime>=endTime:
            timeIntervals.append(endTime)
            return timeIntervals
        timeIntervals.append(newTime)
        previousTime=newTime


def makeTimeIntervalList(timeList):
    timeIntervals=[]
    previousTime=timeList[0]
    for time in timeList[1:]:
        timeInterval=[previousTime,time]
        timeIntervals.append(timeInterval)
        previousTime=time
    return timeIntervals


def getVariable(variableName, startTime,endTime):
    rawData = ldb.get(variableName,startTime,endTime,unixtime=False)
    times,dataPoints = rawData[variableName]
    return times, dataPoints

def getEnergiesAtDump(energyVariableName,startTime,endTime,dumpTimes):
    energiesPP=[]
    energyTimes=[]
    energyData = ldb.get(energyVariableName,startTime,endTime,unixtime=False)
    timesEnergy,allEnergiesPP = energyData[energyVariableName]
    # transform times to floats, like before
    print('search Energies at Dumps ...')
    for i,time in enumerate(dumpTimes):
        dumpTimeId=findIdOfNearest(timesEnergy,time)
        energyTimes.append(timesEnergy[dumpTimeId-1])
        if allEnergiesPP[dumpTimeId-1]<7800:
            energiesPP.append(allEnergiesPP[dumpTimeId-1])
        else:
            energiesPP.append(0)  
    return energyTimes, energiesPP


def findIdOfNearest(array,value):
    idx=(np.abs(array-value)).argmin()
    return idx

def calculateEnergies(dumpTimes,dumpedIntensities,energiesPP):
    print('post process data ...')
    energiesTotal=[i*j*1.602176487E-16 for i,j in zip(dumpedIntensities,energiesPP)]
    integratedEnergies=getIntegratedEnergy(energiesTotal)
    return energiesTotal,integratedEnergies


def getIntegratedEnergy(energies):
    integratedEnergies=[sum(energies[:i])/1000 for i,energy in enumerate(energies)]
    return integratedEnergies


def main():
    startTime = "2011-01-01 00:00:00.000"
    endTime = "2017-11-20 00:00:00.000"

    intensityVariableName = 'CONTEXT.XPOC.B1:I_TO_DUMP'
    energyVariableName= 'BLM.XPOC.B1:E_KICK'

    dumpTimes,dumpedIntensities,energyTimes,energiesPP = getData(startTime,endTime,intensityVariableName,energyVariableName)
    energiesTotal,integratedEnergies = calculateEnergies(dumpTimes,dumpedIntensities,energiesPP)
    print('Plot Data ...')
    # plotting
    plt.subplot(4, 1, 1)
    plt.plot(dumpTimes,energiesTotal, 'b+')
    plt.title('Energy sent to the dump (Beam 1)')
    plt.ylabel('Dumped Energy / MJ')

    plt.subplot(4, 1, 2)
    plt.plot(dumpTimes,integratedEnergies, 'b-')
    plt.title('Integrated Energy sent to the Dump (Beam 1)')
    plt.ylabel('Dumped Energy / GJ')

    plt.subplot(4, 1, 3)
    plt.plot(dumpTimes,dumpedIntensities, 'b+')
    plt.title('CONTEXT.XPOC.B1:I_TO_DUMP')
    plt.ylabel('Intensity')

    plt.subplot(4, 1, 4)
    plt.plot(dumpTimes,energiesPP, 'b+')
    plt.title('BLM.XPOC.B1:E_KICK')
    plt.xlabel('year')
    plt.ylabel('Energy per p+ / GeV')

    plt.show()
if __name__ == '__main__':
    main()