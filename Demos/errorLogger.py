import time, traceback

def logError(err):
    with open('errorLog.txt', 'a+') as file:
        file.write('Error logged at: ' + time.strftime("%H:%M:%S %d-%m-%Y", time.localtime()) + '\n')
        file.write('Error details as printed by python: \n' + str(err) + '\n')

myL = [1,0,2]

for i in myL:
    try:
        print(1/i)
    except Exception:
        logError(traceback.format_exc())
    finally:
        pass
