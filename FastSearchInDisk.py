# Values you can edit here

email = "" # Email /!\ Must be an email.
password = "" # password of acc
defaultletter = "S" # A B C D E F G H I J K L M N O P Q R S T U V W Z Y Z
maxround = 180 # max round allowed until the script stop.
debug = False # True or False
realismmode = True # True or False
websiteurl = "https://www.fest-view.com/" # In case the website url change

# -- Information about the script.
scriptversion = "0.0.1"
scriptname = "FastSeach"

# utils things / basics things 
from logging import error
from typing import KeysView 
from array import array # new

# logs or random letters function librairies required to make the script works
import time
import random
import string
import datetime


# new imports / selenium imports.
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Don't Touch Below

selstar = None

def logintofest():
    try:
        search_btn = driver.find_element_by_id("username")
        search_btn.send_keys(email)
        search_x = driver.find_element_by_id("password")
        search_x.send_keys(password)
        buttonlogin = driver.find_element_by_class_name("button-submit")
        buttonlogin.click()
        return True
    except:
        return False

def check_exists_by_classname(classname):
    try:
        driver.find_element_by_class_name(classname)
    except EC.NoSuchElementException:
        print("Exception")
        return False
    return True

def selectstar():
    time.sleep(.3)
    global defaultletter
    global selstar
    oldrealismmode = None
    global realismmode

    #Searching Stars whose name start with Random Letter    
    time.sleep(.75)
    ids = driver.find_element_by_id("similarArtist")

    if(ids.text != defaultletter):
        ids.send_keys(Keys.CONTROL + "a");
        ids.send_keys(Keys.DELETE);

    #currently testing...
    defaultletter = random.choice(string.ascii_lowercase)

    ids.send_keys(defaultletter)
    time.sleep(3)
   
    #if(driver.find_element_by_id("similarArtist").text == None or driver.find_element_by_id("similarArtist").text == ""):
    #    print("SimilarArtist is Empty, Re-Running Loop.")
    #    selectstar()

    if(realismmode != oldrealismmode):
        print("Resetting RealismMode to " + str(oldrealismmode))
        realismmode = oldrealismmode



    if realismmode == True:

        oldrealismmode = realismmode

        finalstarlists = None
        try:
            liststars = [driver.find_element_by_id("similarArtist-option-0"), driver.find_element_by_id("similarArtist-option-1"), driver.find_element_by_id("similarArtist-option-2"), driver.find_element_by_id("similarArtist-option-3"), driver.find_element_by_id("similarArtist-option-4"), driver.find_element_by_id("similarArtist-option-5"), driver.find_element_by_id("similarArtist-option-6"), driver.find_element_by_id("similarArtist-option-7"), driver.find_element_by_id("similarArtist-option-8"), driver.find_element_by_id("similarArtist-option-9"), driver.find_element_by_id("similarArtist-option-10")]
            finalstarlists = liststars
        except:
            print("Couldn't fill list. Re-Running Loop & disabling RealisMode for this round.\n")
            realismmode = False

        if(finalstarlists == None):
            print("Re-Running Loop.")
            return selectstar()

        if len(finalstarlists) == 0:
            print("\n\033[31m[" + str(datetime.datetime.now()) + "] " + "List of Stars Empty. Re-Running loop. & Randomizing letter\033[0m\n")
            defaultletter = random.choice(string.ascii_lowercase)
            return selectstar()

        if finalstarlists == None:
            print("liststars is None. Re-Running loop.")
            return selectstar()

        valuechoosen = random.randint(0, (len(finalstarlists)-1))
        selstar = finalstarlists[valuechoosen]

        if debug == True:
            print("\n\033[35m Selecting " + valuechoosen + "th Star in the list.\n")
            print("_____________________________\n\nSelected:\n\n" + str(selstar.text) + "\033[0m\n_____________________________\n")

        selstar.click()
        return True
    else:
        #selstar = driver.find_element_by_id("similarArtist-option-0")

        #if selstar != driver.find_element_by_id("similarArtist-option-0"):
        #    print("Re-Running Loop to avoid issue.\n")
        #    return selectstar()

        time.sleep(2)

        if len(driver.find_elements_by_id('similarArtist-option-0')) > 0:
            driver.find_element_by_id("similarArtist-option-0").click()
            return True
        else:
            return selectstar()

    return False


def page_has_loaded():
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'


def loopwin(i):
    while(page_has_loaded() == False):
        time.sleep(.1)
    obou = 0
    beforecoin = None
    aftercoin = None
    
    while True:

        if i == maxround:
            print("Reached Max Round. Exiting.")
            quit()
            
        if realismmode == True:
            if i == 1:
                print("Realism Mode enabled, so random time sleeping.")
                rdmsleeptime = random.randint(1, 10)
                print("Sleeping " + str(rdmsleeptime) + " seconds")
                time.sleep(int(rdmsleeptime))

        sleepingtime = .4

        while(str(driver.current_url) != websiteurl):
            sleepingtime = sleepingtime * 2
            print("URL not valid. Checking in " + str(sleepingtime * 2) + " seconds")
            time.sleep(sleepingtime)

        if EC.presence_of_element_located('navbar-user-points-mobile') != True:
            obou = 0


        selectstar()
        time.sleep(1.1)
        if obou == 1:
            beforecoin = driver.find_element_by_class_name("navbar-user-points-mobile").text

        submitbutton = driver.find_element_by_class_name("button-submit")


        #wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "button-submit")))
        #print(selstar)

        submitbutton.click()


        i = i + 1
        print("\033[4m[" + str(datetime.datetime.now()) + "] Round " + str(i) + "\033[0m\n")
        if obou == 1:
            aftercoin = driver.find_element_by_class_name("navbar-user-points-mobile").text

        time.sleep(2)

        if obou == 1: 
            print("\033[32m\nVous avez " + str(driver.find_element_by_class_name("navbar-user-points-mobile").text) + "Coins.\033[0m\n")

            if beforecoin == aftercoin:
                print("\033[33m" + "/!\ Didn't get any coins. " + " \033[0m")
                print("\033[31m[Feature in Developpment.]\033[0m")
        else:
            obou = 1
        
        if EC.presence_of_element_located('similarArtist-helper-text') != None:
            loopwin(i)




# ============================================================
# -------------------------- Script --------------------------
# ============================================================

print("\n============================================================\n\033[4m" + str(scriptname) + " - V" + str(scriptversion) + "\nBy Zellix#3337 & Lucaas#4656\033[0m\n============================================================\n")


print("\033[34mInitializing Chrome.\033[0m\n")

#Init Chrome & open a tab with the url.
driver = webdriver.Chrome(executable_path="chromedriver.exe")
wait = WebDriverWait(driver, 10)
driver.get("https://www.fest-view.com/artist/create")


# Waiting for the page to finish loading in order to login.
wait.until(lambda driver: driver.current_url != "https://www.fest-view.com/artist/create")
print("[" + str(datetime.datetime.now()) + "] " + " Waiting the page load before login.")


#LOGGING IN

print("\n\n\n\n\n")
print("Logging in...")
boo = logintofest()

if boo == False:
    error("\033[31mCouldn't login.\033[0m")
    exit()
else:
    print("Successfully logged in !")

i = 0
            
loopwin(i)

