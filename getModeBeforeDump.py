import pytimber
ldb = pytimber.LoggingDB()

def printBeamModeBeforeDump(startTime,endTime):
    fills = ldb.getLHCFillsByTime(startTime, endTime, beam_modes='BEAMDUMP',unixtime=False)
    fillsData = [ldb.getLHCFillData(i['fillNumber'],unixtime=False) for i in fills]
    prevmode = ''
    for dumpedFillData in fillsData:
        for mode in dumpedFillData['beamModes']: 
            if 'DUMP' in mode['mode']:
                break
            prevmode = mode['mode']
            t1 = mode['startTime']
            t2 = mode['endTime']
        print('Beam was in mode ' + str(prevmode) +' and there was a ' + str(mode['mode']) + ' at ' + str(mode['startTime']))
    return
def main():
    startTime = "2015-09-16 09:44:39.007"
    endTime = "2015-09-16 12:38:55.784"
    printBeamModeBeforeDump(startTime,endTime)

if __name__ == '__main__':
    main()