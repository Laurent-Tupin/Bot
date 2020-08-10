import random
import time, datetime 
import pandas as pd
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

#------------------------------------------------------------------------------
# Class Selenium
#------------------------------------------------------------------------------
class c_selenium_chrome():
    '''# ----------------------------------------------------
    # To use Chrome Driver
    #  https://chromedriver.chromium.org/
    #  download and UnZip the folder
    #  Move it to Users/local/bin   OR    C:\ProgramData\Anaconda3\Library\bin
    # ----------------------------------------------------'''
    def __init__(self, str_url):
        self.driver = selenium.webdriver.Chrome()
        self.str_url = str_url

    def open(self):
        self.driver.get(self.str_url)
        time.sleep(2)
    
    def closeBrowser(self):
        self.driver.close()
        
    def DefineButton(self, str_buttonxPath):
        self.GoogleObject = self.driver.find_element_by_xpath(str_buttonxPath)

    def Clic(self, str_buttonxPath = None, str_buttonName = '', l_buttonIfFailed = []):
        if not str_buttonxPath is None:     self.DefineButton(str_buttonxPath)
        if str_buttonName.lower() in self.GoogleObject.text.lower():
            self.GoogleObject.click()
        else:
            print(' (+) Link found was not {} but: {}'.format(str_buttonName, self.GoogleObject.text))
            for xPath in l_buttonIfFailed:
                time.sleep(5)
                try:
                    if self.Clic(xPath, str_buttonName, []):
                        print(' (+) Link is: {}'.format(self.GoogleObject.text))
                        break
                    else:   raise
                except:     continue
            return False
        return True
        
    def FillUp(self, str_buttonxPath = None, str_textToFill = ''):
        if not str_buttonxPath is None:     self.DefineButton(str_buttonxPath)
        self.GoogleObject.send_keys(str_textToFill)
        
    def SendEnter(self, str_buttonxPath = None):
        if not str_buttonxPath is None:     self.DefineButton(str_buttonxPath)
        self.GoogleObject.send_keys(Keys.RETURN)
    
    def changeWindow(self, int_nbWindow):
        self.baseWindow = self.driver.window_handles[0]
        self.int_nbWindowsTotal = len(self.driver.window_handles)
        int_nbWindow = int_nbWindow % self.int_nbWindowsTotal
        self.newWindow = self.driver.window_handles[int_nbWindow]
        self.driver.switch_to.window(self.newWindow)
        
    def changeWindowBack(self):
        try:        self.driver.switch_to.window(self.baseWindow)
        except Exception as err:
            print('Could not go back to Base Window... Make sure u used changeWindow before || {}'.format(err))
            try:    self.driver.switch_to.window(self.driver.window_handles[0])
            except: pass
    
    def clicCaptcha(self, str_recaptcha):
        self.str_recaptcha = str_recaptcha
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,
                     "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.str_recaptcha))).click()
    
    
    
class c_Bot_instagram(c_selenium_chrome):
    # Step 1: Init will open Instagram Page
    def __init__(self):
        self.l_uniquePicHref = []
        super().__init__(r'https://instagram.com')
        self.open()
    
    # Step 2. we will Login into Instagram
    def login(self, str_uid, str_pwd):
        try:
            # Find the different place we need in the page 
            str_adrrUid = r'//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input'
            str_adrrPwd = r'//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input'
            str_LOGIN = r'//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div'
            # Action: fill up username and Password, clic Login
            self.FillUp(str_adrrUid, str_uid)
            self.FillUp(str_adrrPwd, str_pwd)
            self.Clic(str_LOGIN)            # or self.SendEnter()
            time.sleep(2)
        except Exception as error: print('login on Instagram did not work || {}',format(error))
    
    def openHashtagPage(self, str_hashTag):
        self.hashTag = str_hashTag
        self.open(r'{}/explore/tags/{}/'.format(self.str_url, str_hashTag))
        time.sleep(2)
    
    def scrollDown(self):
        self.driver.execute("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    
    def GetTagsList(self):
        # IN
        l_uniquePicHref = self.l_uniquePicHref
        self.l_picObj_href = []
        # Get pics on the current page
        l_picObj = self.driver.find_elements_by_tag_name('a')
        l_picObj_href = [elem.get_attribute('href') for elem in l_picObj]
        l_picObj_href = [elem for elem in l_picObj_href if '.com/p/' in elem]
        l_picObj_href = [elem for elem in l_picObj_href if self.hashTag in l_picObj_href]
        # building list of unique photos
        l_picObj_href = [pic for pic in l_picObj_href if pic not in l_uniquePicHref]
        print(" (*) Check: Nb of Pics " + str(len(l_picObj_href)))
        self.l_picObj_href = l_picObj_href
        # Keep only unique for the rest of the Algo
        l_uniquePicHref.extend(l_picObj_href)
        self.l_uniquePicHref = l_uniquePicHref
        
    def like_pic(self, pic_obj):
        self.driver.get(pic_obj)
        self.scrollDown()
        try:
            self.driver.find_element_by_link_text('Like').click()
            time.sleep(18)
        except Exception as error:
            print(' - ERROR in like_pic: {}'.format(error))
            time.sleep(2)
        
    def Loop_like_pic(self, str_hashTag, int_hourProcess = 1):
        t_start = datetime.datetime.now()
        while t_start:
            self.openHashtagPage(str_hashTag)
            self.scrollDown()
            self.GetTagsList()
            for pic in self.l_picObj_href:
                self.like_pic(pic)
            # EXIT 
            t_now = datetime.datetime.now()
            if (t_now - t_start).seconds / 3600 > int_hourProcess:
                t_start = False     


# Parameters
str_path = r'C:\Users\Laurent.Tu\Documents\Apprendre Program\Python\Archive\Secret.csv'
df_uid = pd.read_csv(str_path)
str_username = df_uid.loc[df_uid['Platform'] == 'instagram', 'Uid'].values[0]
str_pwd = df_uid.loc[df_uid['Platform'] == 'instagram', 'Password'].values[0]
l_hashtag = ['GuineaPigs', 'Guinea']


# Launch the BOT
bot = c_Bot_instagram()    
bot.login(str_username, str_pwd)
while True:
    hashTag = random.choice(l_hashtag)
    print('HashTag:', hashTag)
    try:
        bot.Loop_like_pic(hashTag, 2)
        time.sleep(5)
    except Exception as error:
        print(' ERROR. will re-start a new Chrome page ||| ', error)
        bot.closeBrowser()
        time.sleep(60)
        bot = c_Bot_instagram()    
        bot.login(str_username, str_pwd)
bot.closeBrowser()



    
#=============================================================    
# Example how to launch a simple google page, search and enter
#=============================================================
def Launch_FirstInstance():
    # Define Parameters
    str_url =  r'https://google.com'
    str_buttonxPath = r'//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input'
    str_text = r'Monthy Python'
    
    # Create an instance (only __init__ will be launch)
    inst_Chrome = c_selenium_chrome(str_url)
    
    # Make this instance doing ACTIONS
    inst_Chrome.open()
    inst_Chrome.FillUp(str_buttonxPath, str_text)
    inst_Chrome.SendEnter(str_buttonxPath)

#Launch_FirstInstance()




    













