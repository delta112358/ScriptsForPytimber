import pytimber
import numpy as np
import datetime
ldb = pytimber.LoggingDB()
import matplotlib.pyplot as plt
from matplotlib import dates

def getData(startTime,endTime,variableName):
    startTime=datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S.%f")
    endTime=datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S.%f")
    print('getting data ...\n')
    data = ldb.get(variableName, startTime, endTime,unixtime=False)
    x,y=data[variableName]
    print('extracting data ...\n')
    return x,y

def main():
    startTime = "2017-03-01 03:00:00.000"
    endTime = "2017-05-01 03:20:00.000"

    intensityVariableName = 'CONTEXT.XPOC.B1:I_TO_DUMP'
    energyVariableName= 'BLM.XPOC.B1:E_KICK'

    x,y=getData(startTime,endTime,'CONTEXT.XPOC.B1:I_TO_DUMP')
    plt.subplot(3, 1, 1)
    plt.plot(x,y,'b-')
    plt.title('CONTEXT.XPOC.B1:I_TO_DUMP')
    plt.ylabel('Intensity')

    x,y=getData(startTime,endTime,'BLM.XPOC.B1:E_KICK')
    plt.subplot(3, 1, 3)
    plt.plot(x,y, 'b-')
    plt.title('BLM.XPOC.B1:E_KICK')
    plt.ylabel('Energy / GeV')
    plt.xlabel('time in month-day hour')

    plt.show()

if __name__ == '__main__':
    main()