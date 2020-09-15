import sys
import json
import re
from pathlib import Path
from selenium import webdriver


#read input
errmsg = "Usage: python3 solver.py { today | yyyy-mm-dd }"
if (len(sys.argv) != 2):
    sys.exit(errmsg)
elif sys.argv[1] != 'today' and re.match('^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$', sys.argv[1]) is None:
    sys.exit(errmsg)

byDate = False
today = False
date = ''
if sys.argv[1] == 'today':
    today = True
else:
    byDate = True
    date = sys.argv[1]



if today:
    #set headless chrome
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")

    #open spelling bee
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    #driver = webdriver.Chrome('./chromedriver.exe')
    url = 'https://www.nytimes.com/puzzles/spelling-bee'
    driver.get(url)

    #grab game data from window and close
    data = driver.execute_script("return window.gameData[\"today\"]")
    outerLetters = ''.join(data['validLetters'])
    centerLetter = data['centerLetter']
    printDate = data['printDate']
    answers = data['answers']
    pangrams = data['pangrams']

    driver.quit()

    #search dictionary words
    esWords = []
    with open("words.txt") as f:
        for line in f: 
            line = line.lower()
            line = line.rstrip()
            if len(line) >= 4:
                if line.find(centerLetter) != -1:
                    if not any(c not in (outerLetters + centerLetter) for c in line):
                        if line not in esWords:
                            esWords.append(line)

    #find words not in answers and words not in dictionary
    notInAnswers = []
    notInDict = []
    for word in esWords:
        if word not in answers:
            notInAnswers.append(word)

    for word in answers:
        if word not in esWords:
            notInDict.append(word)

    #calculate points
    possiblePoints = 0
    byPoint = {}
    for answer in answers:
        if answer not in pangrams:
            length = len(answer)
            if length == 4:
                length = 1
            if length not in byPoint:
                byPoint[length] = [answer]
            else:
                byPoint[length].append(answer)
            possiblePoints += length

    for pangram in pangrams:
        if len(pangram) + 7 not in byPoint:
            byPoint[len(pangram) + 7] = [pangram]
        else:
            byPoint[len(pangram) + 7].append(pangram) 
        possiblePoints += len(pangram) + 7

    #archive dict
    archiveData = {}
    archiveData['outerLetters'] = outerLetters
    archiveData['centerLetter'] = centerLetter
    archiveData['printDate'] = printDate
    archiveData['answers'] = answers
    archiveData['pangrams'] = pangrams
    archiveData['byPoint'] = byPoint
    archiveData['possiblePoints'] = possiblePoints
    archiveData['notInAnswers'] = notInAnswers
    archiveData['notInDict'] = notInDict


    #make archive file
    if not Path("archive/" + archiveData['printDate'] + ".txt").is_file():

        with open("archive/" + archiveData['printDate'] + ".txt", "w") as f:
            json.dump(archiveData, f)
    else:
        print("In Archive!")

elif date:
    archiveData = {}
    if Path("archive/" + date + ".txt").is_file():
        with open("archive/" + date + ".txt", "r") as f:
            archiveData = json.load(f)
    else:
        print(date, "puzzle not in the archive sorry!")
        sys.exit()



#print output
print("------------NYT SPELLING BEE " + archiveData['printDate'] +  "------------")
print("Words By Point Value: ")
for point, words in archiveData['byPoint'].items():
    print(point, "point words:")
    for word in words:
        print(word)

print('Dictionary words not in puzzle: ')
for word in archiveData['notInAnswers']:
    print(word)
print('Puzzle words not in my dictionary: ')
for word in archiveData['notInDict']:
    print(word)

print(len(archiveData['answers']), "words pissible for a total of", archiveData['possiblePoints'], "possible points!")
print("------------NYT SPELLING BEE " + archiveData['printDate'] +  "------------")




#How  I was trying to do it before I realized the answers are litteraly in the webpage lol
'''
#click play button
stbutton = driver.find_element_by_xpath('//*[@id="portal-game-modals"]/div/div/div/div/div/div/div[3]/button')
stbutton.click()

#function to check if subscribe button appears
def check_element(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

#set letters
lts = ''
clt= ''
content = driver.find_element_by_xpath('//*[@id="pz-game-root"]/div/div[1]/div').text.lower()

for line in content.splitlines():
    line = line.lstrip()
    if(len(line) == 1):
        lts += line

clt = lts[0]
lts = lts[1:]
print("Center Letter:", clt)
print("Other Letters:", lts)


#search
words = []
with open("words.txt") as f:
    for line in f: 
        line = line.lower()
        line = line.rstrip()
        if len(line) >= 4:
            if line.find(clt) != -1:
                if not any(c not in (lts + clt) for c in line):
                    if line not in words:
                        words.append(line)


if check:
    print("Checking", len(words), "possible words ... ")

    #sort words by length
    words.sort(key=len)
    keysTo = driver.find_element_by_tag_name('body')
    correctWords = []

    for word in words:
        if not check_element('//*[@id="portal-game-modals"]/div/div/div/div'):
            keysTo.send_keys(Keys.ENTER)
            keysTo.send_keys(word)
            keysTo.send_keys(Keys.ENTER)
            while (driver.find_element_by_xpath('//*[@id="pz-game-root"]/div/div[1]/div/div[1]').text != ''):
                time.sleep(.1)
            
        else:
            works = driver.find_element_by_xpath('//*[@id="pz-game-root"]/div/div[2]/div[2]/div[2]/div/div/ul').text.lower()
            for line in works.splitlines():
                correctWords.append(line)
            driver.quit()
            driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
            #driver = webdriver.Chrome('./chromedriver.exe')
            driver.get(url)
            print("Currently on:", word)
            stbutton = driver.find_element_by_xpath('//*[@id="portal-game-modals"]/div/div/div/div/div/div/div[3]/button')
            stbutton.click()
            keysTo = driver.find_element_by_tag_name('body')
            keysTo.send_keys(Keys.ENTER)
            keysTo.send_keys(word)
            keysTo.send_keys(Keys.ENTER)
            while (driver.find_element_by_xpath('//*[@id="pz-game-root"]/div/div[1]/div/div[1]').text != ''):
                time.sleep(.1)
            

    driver.quit()

    doubleCheck = []
    for word in words:
        if word not in correctWords:
            print(word)
            doubleCheck.append(word)

    print("Double Checking", str(len(doubleCheck)), "words!")

    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    #driver = webdriver.Chrome('./chromedriver.exe')
    driver.get(url)
    stbutton = driver.find_element_by_xpath('//*[@id="portal-game-modals"]/div/div/div/div/div/div/div[3]/button')
    stbutton.click()
    
    for word in doubleCheck:
        if not check_element('//*[@id="portal-game-modals"]/div/div/div/div'):
            keysTo.send_keys(Keys.ENTER)
            keysTo.send_keys(word)
            keysTo.send_keys(Keys.ENTER)
            while (driver.find_element_by_xpath('//*[@id="pz-game-root"]/div/div[1]/div/div[1]').text != ''):
                time.sleep(.1)
            
        else:
            works = driver.find_element_by_xpath('//*[@id="pz-game-root"]/div/div[2]/div[2]/div[2]/div/div/ul').text.lower()
            for line in works.splitlines():
                if line not in correctWords:
                    print("Double Check!")
                    correctWords.append(line)
            driver.quit()
            driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
            #driver = webdriver.Chrome('./chromedriver.exe')
            driver.get(url)
            print("Currently on:", word)
            stbutton = driver.find_element_by_xpath('//*[@id="portal-game-modals"]/div/div/div/div/div/div/div[3]/button')
            stbutton.click()
            keysTo = driver.find_element_by_tag_name('body')
            keysTo.send_keys(Keys.ENTER)
            keysTo.send_keys(word)
            keysTo.send_keys(Keys.ENTER)
            while (driver.find_element_by_xpath('//*[@id="pz-game-root"]/div/div[1]/div/div[1]').text != ''):
                time.sleep(.1)

    

    #sort, parse, and print data
    correctWords.sort()
    for word in correctWords:
        print(word.upper())
    correctWords.sort(key=len)


    curL = 4
    panagrams = []
    print('4 Letter Words: ')

    for word in correctWords:
        if set(word) >= set(lts):
            panagrams.append(word)

        elif len(word) == curL:
            print(word)
        else:
            curL = len(word)
            print(curL, 'Letter Words: ')
            print(word)

    print('PANAGRAMS: ')
    for panagram in panagrams:

        print(panagram)

    print("Found" , len(correctWords), "words!")

else:
    driver.quit()
    #sort, parse, and print data
    words.sort()
    words.sort(key=len)


    curL = 4
    panagrams = []
    print('4 Letter Words: ')

    for word in words:
        if set(word) >= set(lts):
            panagrams.append(word)

        elif len(word) == curL:
            print(word)
        else:
            curL = len(word)
            print(curL, 'Letter Words: ')
            print(word)

    print('PANAGRAMS: ')
    for panagram in panagrams:

        print(panagram)

    print("Found" , len(words), "potential words!")
    '''