import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


#read input
'''
errmsg = "Usage: python3 solver.py { 6 lowercase and 1 uppercase letter no spaces }"
if (len(sys.argv) != 2):
    sys.exit(errmsg)

allLetters = sys.argv[1]

lts = ''.join([x for x in allLetters if x.islower()])
if (len(lts) != 6):
    sys.exit(errmsg)

clt = ''.join([x for x in allLetters if x.isupper()])
if (len(clt) != 1):
    sys.exit(errmsg)

clt = clt.lower()
'''

#set headless chrome
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")

#open spelling bee
driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
url = 'https://www.nytimes.com/puzzles/spelling-bee'
driver.get(url)

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

print("Checking", len(words), "possible words ... ")

#sort words by length
words.sort(key=len)
keysTo = driver.find_element_by_tag_name('body')
correctWords = []


for word in words:
    if not check_element('//*[@id="portal-game-modals"]/div/div/div/div'):
        keysTo.send_keys(word)
        keysTo.send_keys(Keys.ENTER)
    else:
        works = driver.find_element_by_xpath('//*[@id="pz-game-root"]/div/div[2]/div[2]/div[2]/div/div/ul').text.lower()
        for line in works.splitlines():
            correctWords.append(line)
        driver.quit()
        driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
        driver.get(url)
        print("Currently on:", word)
        stbutton = driver.find_element_by_xpath('//*[@id="portal-game-modals"]/div/div/div/div/div/div/div[3]/button')
        stbutton.click()
        keysTo = driver.find_element_by_tag_name('body')
        keysTo.send_keys(word)
        keysTo.send_keys(Keys.ENTER)
        

driver.quit()



#sort, parse, and print data
correctWords.sort()
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