#imports modules and libraries needed for the project to run
import eel, time, random
from datetime import datetime
logging = True
logFile ='defaultLog.log'
variables = {}
#Checks that values are in allowed range
def checkValues(x, y):
    if x>=0 and x<= 135 and y>= 0 and y<=70:
        return True
    else:
        return False
#Draws the vertical diagram of the antenna
def draw(angle):
    eel.draw(angle)
#Returns the current position of the antenna in x or y coordinates depending on the function
def returnX():
    return eel.returnPos()()[0]
def returnY():
    return eel.returnPos()()[1]
#parses data received via the GUI command line or via script
@eel.expose
def recieve(data, line):
    cleanedData = data.replace('\n', '')
    send(cleanedData)
    if 'move' in cleanedData:
        fixed = cleanedData.replace('move ', '').split(' ')
        try:
            command = 'G0 ' + fixed[0] + ' ' + fixed[1]
        except IndexError:
            send('INVALID MOVE COMMAND')
        start(command)
    elif 'save' in cleanedData:
        saveInfo = cleanedData.replace('save ', '').split(' ')
        try:
            save(saveInfo[0], str(saveInfo[1]), str(saveInfo[2]))
        except IndexError:
            send("INVALID SAVE COMMAND")
    elif 'stow' in cleanedData:
        stow()
    elif 'load' in cleanedData:
        load(cleanedData.replace('load ', ''))
    elif 'begin'  in cleanedData:
        begin(cleanedData.replace('begin', '').replace(" ", ''))
    elif 'end' in cleanedData:
        send("CLOSING THE LOG FILE")
        send("ENDING DATA COLLECTION")
        global logging
        logging = False
    elif 'collect' in cleanedData:
        location =  cleanedData.replace('collect ', '').split(' ')[0]
        delay =  cleanedData.replace('collect ', '').split(' ')[1]
        collect(str(location), float(delay))
    elif cleanedData in variables.keys():
        savedCommand = 'G0 ' +  variables[cleanedData].split(",")[0] + ' ' + variables[cleanedData].split(",")[1]
        start(savedCommand)
    else:
        send("INVALID COMMAND")
        if line != 0:
            send("ERROR ON LINE " + str(line))
            send("GOING TO NEXT LINE IN 2 SECONDS")
            time.sleep(2)
#sends data to the GUI console output
def send(data):
    log(data)
    eel.update(str(data))
#updates the current position of the antennnae
def updateCurrentPos(currX, currY):
    eel.updateCurr(currX, currY)
    draw(currX)
#starts movement of antenna
@eel.expose
def start(command):
    x, y = parse(command)
    emulateMovement(x, y, returnX(), returnY(), command)
    send('NEW POSITION AT ' + str(x) + ',' + str(y))
    updateCurrentPos(x, y)
#returns the antenna to the position 0 0
def stow():
    send("RESETING TO POSITION 0, 0")
    emulateMovement(0, 0, returnX(), returnY(), "G0 0 0")
    updateCurrentPos(0, 0)
    send('NEW POSITION AT ' + str(0) + ',' + str(0))
    send('SHUTTING DOWN ANTENNA UNTIL GIVEN A NEW COMMAND')
    send('A0 OFF')
#checks and parses the command
def parse(code):
    #returns specific x,y values
    parsed = code.replace('G0 ', '').split(' ')
    if len(parsed) != 2:
        print('INVALID GCODE COMMAND')
        send('INVALID GCODE COMMAND')
    if checkValues(float(parsed[0]), float(parsed[1])):
        x = float(parsed[0])
        y = float(parsed[1])
        return x, y
    else:
        send('COMMAND IS NOT IN THE ALLOWED RANGE OF MOTION')
#emulates the time for movement 5 seconds/degree
def emulateMovement(x, y, currX, currY, command):
    if(x-currX >= 0):
        xDiff = str(x-currX)
    else:
        xDiff = str((x-currX)*-1)
    if(y-currY>=0):
        yDiff = str(y-currY)
    else:
        yDiff = str((y-currY)*-1)
    maximum = max(float(xDiff), float(yDiff))
    send("CURRENT POSITION " + str(currX) +"," + str(currY) + "    ")
    send("EXECUTING COMMAND " + command  + "    ")
    send("MOVING TO " + str(x) + ',' + str(y) +' : estimated time: ' + str(maximum*5) + " seconds"   + "     ")
    time.sleep(maximum*5)
#loads a script
def load(loc):
    try:
        code = open(loc, "r").readlines()
        send('READING FILE..' )
    except FileNotFoundError:
        send('THE FILE COULD NOT BE FOUND')
        send('PLEASE CHECK YOUR SPELLING')
    line = 0
    for data in code:
        line += 1
        recieve(data, line)
#logs all interface data to a location
def log(data):
    if logging != False:
        with open(logFile, "a") as log:
            now = datetime.now()
            currentTime = now. strftime("%H:%M:%S")
            log.write("\n" + currentTime + "  " + str(data))
#initiates logging when called
def begin(loc):
    global logging
    logging = True
    if(len(loc) < 3):
        send('WARNING: NO LOG LOCATION SET: USING DEFAULT')
    else:
        global logFile
        logFile = str(loc)
        send('DATA LOGGING ENABLED: LOG LOCATION: ' + str(loc))
#collects randomly generated data and moves the antenna to automatically to record drifting data
def collect(loc, delay):
    send('COLLECTING DATA AT LOCATION ' + str(returnX()) + ", " + str(returnY()))
    with open(loc, "a") as log:
        numValues = delay / 5
        for i in range(int(numValues)): 
            time.sleep(5)
            if ((i+1)*5) % 240 == 0:
                send('AUTOMATICALLY MOVING ANTENNA TO COUNTER ACT DRIFTING OBJECTS')
                start("G0 " + str(returnX()+1) + " " + str(returnY()))
            currentTime = datetime.now().strftime("%H:%M:%S")
            for t in range(96):
                send(currentTime + "  " + str(random.randint(115000, 130000)))
                log.write("\n" + currentTime + "  " + str(random.randint(115000, 130000)))
    send('DATA COLLECTION COMPLETE')
#saves a user defined variable to be used later
def save(variable, x, y):
    send('STORING VALUE ' + variable)
    variables[variable] = x + "," + y
@eel.expose
def generateScript(data, loc):
    with open(loc, 'w') as script:
        script.write(data)
    send('Generating Script')
#sets up front-end GUI interface folder
eel.init('web')
#starts the program with the proper main GUI interface
eel.start('main.html')