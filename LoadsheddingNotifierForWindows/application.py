from selenium import webdriver
from pynput.keyboard import Key, Controller
from lxml import html
from playsound import playsound
import subprocess
import datetime
import requests
import time
from sys import *
import re
import os

place = 'Philadelphia'
pathToProgramDirectory = os.getcwd()
pathToChromeDriver = f'{pathToProgramDirectory}\chromedriver.exe'


# File paths
fifteenAudio = f'{pathToProgramDirectory}\Audio\\fifteen.mp3'
tenAudio = f'{pathToProgramDirectory}\Audio\\ten.mp3'
fiveAudio = f'{pathToProgramDirectory}\Audio\\five.mp3'
notification = f'{pathToProgramDirectory}\Audio\\notification.mp3'

def main():
    
    isThereLoadshedding = True
#                           ^ This should be false
    
    # The main loop
    scriptActivity = True
    while scriptActivity:
        
        # ---------------------------------------------------------------------------------------------------------------
        
        # Checking if there is loadshedding at the moment
        if DiscoverLoadsheddingStatus():
            isThereLoadshedding = True
        
        # ---------------------------------------------------------------------------------------------------------------
        
        # Do nothing if loadshedding is not happening right now
        if isThereLoadshedding == False:
            print('There is no loadshedding')
            pass
        else:
            # Getting the time set on the system (Mainly used to check the date)
            System_time = time.asctime(time.localtime(time.time()))

            print(time.asctime(time.localtime(time.time())))
            today = datetime.datetime.now()
            print(today.strftime("%m/%d/%Y, %H:%M:%S"))
            
            # The directory to the file with the information from the website
            fileDirectory = f'{pathToProgramDirectory}\Results\\times.txt'
            # The direcotry to the file with the information from the website
            fileDirectory2 = f'{pathToProgramDirectory}\Results\\times2.txt'
            # Checking if the file can be opened (a.k.a if it is there)
            try:
                f = open(fileDirectory)
                f.close()
            except:
                f = open(fileDirectory, 'w')
                f.write('N/A' + '\n' + 'N/A')
                f.close()
            
            # Check if the date on the information is correct 
            if DateCheck(System_time, fileDirectory) == False:
                UpdateInfo()
            
            # Putting the times from the file into memory (in the times list)
            times = []
            with open(fileDirectory) as info:
                for line in info:
                    times.append(line)
            del times[0]
            hasBeenRemoved = False
            with open(fileDirectory2) as info:
                for line in info:
                    if hasBeenRemoved == False:
                        hasBeenRemoved = True
                    else:
                        times.append(f'{int(line[0:2]) + 24}{line[2:8]}{int(line[8:10]) + 24}{line[10:]}')

            print(times)
            
            # Finding what the time is right now
            currentTime = GetTheTime()[0]
            
            # checking if there is an approaching loadshedding period
            if not TimeBeforeLoadshedding(currentTime, times):
                print('All scheduled times for today have passed')
                pass
            else:
                approachingTime = True
                
                # Setting the variables checking if the warning audio has been played
                fifteenPlayed = False
                tenPlayed = False
                fivePlayed = False
                
                while approachingTime:
                    print(f'system time right now: {time.asctime(time.localtime(time.time()))[11:19]}')
                    timeDict = TimeBeforeLoadshedding(f"{int(time.asctime(time.localtime(time.time()))[11:13]) + 2}{time.asctime(time.localtime(time.time()))[13:19]}", times)
                    print(f'timeDict = {timeDict}')
                    
                    if timeDict['hours'] == 0:

                        if timeDict['minutes'] == 15:
                            if fifteenPlayed == False:
                                playsound(notification)
                                playsound(fifteenAudio)
                                print('File played')
                                fifteenPlayed = True

                        elif timeDict['minutes'] == 10:
                            if tenPlayed == False:
                                playsound(notification)
                                playsound(tenAudio)
                                print('File played')
                                tenPlayed = True

                        elif timeDict['minutes'] == 5:
                            if fivePlayed == False:
                                playsound(notification)
                                playsound(fiveAudio)
                                print('File played')
                                fivePlayed = True
                                
                                # Shutting down the computer
                                print('Executing shutdown command')
                                time.sleep(1)
                                os.system("shutdown /h")
                                #            ^ remove this echo

                    time.sleep(30)

        # Killing the main loop
        #scriptActivity = False

        # Looping through the main loop every hour
        time.sleep(3600)


def TimeBeforeLoadshedding(systemTime, recordTimeList):
    '''
    system_time is currentTime in the main function

    Shows you how long it is before the next powercut
    
    Returns: dictionary containing ['hours'] and ['minutes']/ False if not
    '''
    
    # Removing the seconds from the system time
    systemTime = systemTime[:-3]
    
    # just stuff that must go
    chuckables = []
    
    # Checking if the time range is not there (aka. There was no schedule for today)
    for time in recordTimeList:
        print(time)
        if time == 'N/A':
            print(time)
            return False
    
    # Checking if that time range has passed and removing the time if it has
    for time in recordTimeList:
        loadsheddingEndTime = time[8:-1]
        if loadsheddingEndTime[:2] == '00':
            loadsheddingEndTime = '24' + loadsheddingEndTime[2:]

        # Breaking the times into numbers I can use
        currentTimeHours = int(systemTime.split(':')[0])
        currentTimeMin = int(systemTime.split(':')[1])

        loadsheddingTimeHours = int(loadsheddingEndTime.split(':')[0])
        loadsheddingTimeMin = int(loadsheddingEndTime.split(':')[1])
        
        # Check if the loadshedding time has already passed
        if loadsheddingTimeHours < currentTimeHours:
            chuckables.append(time)
        elif loadsheddingTimeHours == currentTimeHours and loadsheddingTimeMin <= currentTimeMin:
            chuckables.append(time)
            
    # Removing the times that have already passed
    for item in chuckables:
        recordTimeList.remove(item)
        
    # Checking if the range of time is currently happening
    for time in recordTimeList:
        loadsheddingEndTime = time[8:-1]
        if loadsheddingEndTime[:2] == '00':
            loadsheddingEndTime = '24' + loadsheddingEndTime[2:]
            
        loadsheddingStartTime = time[0:5]
        if loadsheddingStartTime[:2] == '00':
            loadsheddingStartTime = '24' + loadsheddingStartTime[2:]
            
        # Breaking the times into numbers I can use
        currentTimeHours = int(systemTime.split(':')[0])
        currentTimeMin = int(systemTime.split(':')[1])

        loadsheddingTimeEndHours = int(loadsheddingEndTime.split(':')[0])
        loadsheddingTimeEndMin = int(loadsheddingEndTime.split(':')[1])
        
        loadsheddingTimeStartHours = int(loadsheddingStartTime.split(':')[0])
        loadsheddingTimeStartMin = int(loadsheddingStartTime.split(':')[1])
        
        # Checking if the current times hours fall withing those of the loadshedding hours
        if not (((currentTimeHours*60)+currentTimeMin) in range(((loadsheddingTimeStartHours*60)+loadsheddingTimeStartMin), ((loadsheddingTimeEndHours*60)+loadsheddingTimeEndMin))):
            print('There is not an inbetween')
            
            # Getting the amount of minutes untill the next powercut
            timeUntillMin = ((loadsheddingTimeStartHours * 60) + loadsheddingTimeStartMin)-((currentTimeHours * 60) + currentTimeMin)
            
            # Converting the until time into hours and minutes
            hoursAndMin = {}
            
            if timeUntillMin >= 60:
                hoursAndMin['hours'] = timeUntillMin // 60
                for _ in range(hoursAndMin['hours']):
                    timeUntillMin -= 60
                hoursAndMin['minutes'] = timeUntillMin
            else:
                hoursAndMin['hours'] = 0
                hoursAndMin['minutes'] = timeUntillMin
            
            return hoursAndMin
            
        # If it is found that the pi is seeing itself working within loadshedding hours then it should do nothing
        else:
            print('There is an inbetween')
            return False
            
            
def DiscoverLoadsheddingStatus():
    '''
    Finds if there is loadshedding or not active
    Returns: True if there is loadshedding/False if there is none
    '''
    eskomPage = requests.get('https://loadshedding.eskom.co.za')
    time.sleep(3)
    tree = html.fromstring(eskomPage.content)
    status = tree.xpath('//*[@id="lsstatus"]/text()')
    if status[0] == ' not Load Shedding':
        return False
    else:
        return True
            
def UpdateInfo():
    '''
    Repeatedly checks if the information has been updated
    Returns: Nothing
    '''
    informationRetrieved = False
    
    while informationRetrieved == False:
        if DataExtractor() == True:
            informationRetrieved = True

def GetTheTime():
    '''
    Retrieving the true time
    Returns: The time
    '''
    realTimePage = requests.get('https://www.timeanddate.com/worldclock/south-africa/cape-town')
    tree = html.fromstring(realTimePage.content)
    timeRightNow = tree.xpath('//*[@id="ct"]/text()')
    return timeRightNow

def DateCheck(SysTime, fileDirectory):
    '''
    Checking if the date on the system is the same as the date on the retrieved information
    Returns: True/False
    '''
    with open(fileDirectory) as info:
        
        sysDateParts = SysTime[0:11].split(' ')
        sysDate = f'{sysDateParts[0]}, {sysDateParts[2]} {sysDateParts[1]}'
            
        lines = []
        for line in info:
            lines.append(line[:-1])
            break
        
        if str(lines[0]) == str(sysDate):
            print('The Dates match')
            return True
        else:
            print("The Dates Don't match")
            return False

def WriteToFile(filename, info, mode):
    '''
    Writing files with the provided file name
    Returns: Nothing
    '''
    f = open(f'{filename}', f'{mode}')
    f.write(info)
    f.close()

def FindTheInfomation(informationfile):
    '''
    Takes the raw information from the website and extract the parts we need and save it as a file called times.txt
    Returns: Nothing
    '''
    loot = []
    with open(informationfile) as raw:
        for line in raw:
            loot.append(re.findall(r'\w\w\w,\s\d\d\s\w\w\w', line))
            loot.append(re.findall(r'\d\d:\d\d\s-\s\d\d:\d\d', line))

    if informationfile == "information.txt":
        f = open(f'{pathToProgramDirectory}\Results\\times.txt', 'w')
    else:
        f = open(f'{pathToProgramDirectory}\Results\\times{informationfile[-5]}.txt', 'w')

    for entry in loot:
        if len(entry) == 0:
            pass
        else:
            f.write(entry[0] + '\n')
    f.close()
    
def DataExtractor():
    '''
    This function is responsible for retrieving the times for loadshedding
    Returns: True/False
    '''
    
    keyboard = Controller()

    driver = webdriver.Chrome(pathToChromeDriver)

    driver.get('https://loadshedding.eskom.co.za')

    time.sleep(4)

    inputField = driver.find_element_by_xpath('//*[@id="suburbSearch"]')
    inputField.send_keys(place)

    time.sleep(4)
    for _ in range(6):
        keyboard.tap(Key.down)
    keyboard.tap(Key.enter)

    time.sleep(5)
    
    # Checking if the website tells you there is no loadshedding schedual
    try:
        notice = driver.find_element_by_xpath('//*[@id="munic1"]/div/div')
        print('There is no scedule for today on the website')
        
        WriteToFile("information.txt", "-", "w")
        
        driver.close()
        
        return True
    except:
        try:
            elem = driver.find_element_by_xpath('//*[@id="schedulem"]/div/div[3]')

            elem2 = driver.find_element_by_xpath('//*[@id="schedulem"]/div/div[4]')
            
            info2 = elem2.get_attribute('innerHTML')

            info = elem.get_attribute('innerHTML')

            WriteToFile("information2.txt", info2, "w")

            WriteToFile("information.txt", info, "w")

            FindTheInfomation("information.txt")

            FindTheInfomation("information2.txt")

            driver.close()

            return True
        except:
            return False

    
main()