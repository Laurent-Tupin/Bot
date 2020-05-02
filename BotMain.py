import time
import pandas as pd
import fct_html as html


#==============================================================
# THEICE for Gold Price
#==============================================================
class c_botTheice(html.c_Selenium_InteractInternet):
    def __init__(self):
        self.str_url = r'https://www.theice.com/marketdata/reports/178'
        super().__init__(self.str_url)
        super().open()
        
    def clicCaptcha_Wait_Validate(self):
        self.str_recaptchaAddress = r'//*[@id="recaptcha-anchor"]'      #"//span[@id='recaptcha-anchor']"
        super().clicCaptcha(self.str_recaptchaAddress)
        print('You will have 90 seconds in case you need to validate Images for Google')
        time.sleep(90)
        self.str_recaptchaValidate = r'//*[@id="reportCenterRecaptchaForm"]/input'
        try:        super().clic('', self.str_recaptchaValidate, [])
        except:     print('ERROR: Did you validate Manually ?')

# Function to launch        
def LaunchTheiceBot():
    # Open Page
    try:        bot = c_botTheice()
    except:     return None, 'Error on Open Page'
    
    # CLick on Captcha
    try:        bot.clicCaptcha_Wait_Validate()
    except:     return bot, 'Error on CLick on Captcha'
    
    return bot, 'END'


#==============================================================
# Tinder for fun example
#==============================================================
class c_tinBot(html.c_Selenium_InteractInternet):
    def __init__(self):
        self.str_url = r'https://tinder.com'
        super().__init__(self.str_url)
        super().open()
        
    def loginFacebook(self, str_uid, str_pass):
        # Click to login facebook
        self.str_xPath = r'//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button'
        self.l_clickXPathIfFailed = [r'//*[@id="modal-manager"]/div/div/div/div/div[3]/span/button'
                                     ,r'//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[3]/button'] 
        super().clic('facebook', self.str_xPath, self.l_clickXPathIfFailed)
        # Login facebook
        super().changeWindow(1)
        super().fillUp(r'//*[@id="email"]', str_uid)
        super().fillUp(r'//*[@id="pass"]', str_pass)
        super().clic('', r'//*[@id="loginbutton"]', [])
        super().changeWindowBack()
        
    def clearPopUpAfterId(self):
        time.sleep(10)
        try:        super().clic('', r'//*[@id="content"]/div/div[2]/div/div/div[1]/button', [])
        except:     print('Not FOUND on I accept cookies')
        time.sleep(30)
        try:        super().clic('', r'//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]', [])
        except:     print('Not FOUND on 1 ALLOW Location')
        try:        super().clic('', r'//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]', [])
        except:     print('Not FOUND on 2 Enable Notifications')
        try:        super().clic('', r'//*[@id="modal-manager"]/div/div/div[2]/button[1]', [])
        except:     print('Not FOUND on 3')
        
    def like(self):
        time.sleep(1)
        self.str_likeButton = r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button'
        super().clic('', self.str_likeButton, [])
        
    def closeMatchPopUp(self):
        time.sleep(1)
        self.str_closePopUpButton = r'//*[@id="modal-manager"]/div/div/div[2]/button[2]'
        self.str_closeMatchButton = r'//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a'
        try:
            super().clic('', self.str_closePopUpButton, [])
            print('Just closed Pop-up after {} LIKE'.format(str(self.i_like)))
        except:
            super().clic('', self.str_closeMatchButton, [])
            print('Just closed Match Pop-up after {} LIKE'.format(str(self.i_like)))
        
    def likeLoop(self):
        time.sleep(30)
        self.i_compteur = 0
        self.i_like = 0
        for i in range(10000):
            try:
                self.like()
                self.i_like += 1
            except:
                self.closeMatchPopUp()
            finally:
                self.i_compteur = i
        print('Loop is over successfully after {} LIKES and {} on the loop'.format(str(self.i_like), str(self.i_compteur)))

# Function to launch
def LaunchTinBot():
    # Open Page
    try:        bot = c_tinBot()
    except:     return None, 'Error on Open Page'
    
    # Login facebook
    try:
        str_path = r'C:\Users\Laurent.Tu\Documents\Apprendre Program\Python\Archive\Secret.csv'
        df_uid = pd.read_csv(str_path)
        str_uid = df_uid.loc[df_uid['Platform'] == 'facebook', 'Uid'].values[0]
        str_pass = df_uid.loc[df_uid['Platform'] == 'facebook', 'Password'].values[0]
    except:     return bot, 'Error on Secret CSV to DF'
    try:        bot.loginFacebook(str_uid, str_pass)
    except:     return bot, 'Error on login facebook'
    
    # Clear Pop-Up
    bot.clearPopUpAfterId()
    
    # Like Loop
    try:        bot.likeLoop()
    except: 
        print('ERROR Loop is over after {} LIKES and {} on the loop'.format(str(bot.i_like), str(bot.i_compteur)))
#        bot.driver.close()
    
    return bot, 'END'



#==============================================================
# Function to launch
#==============================================================
bot, str_returnMsg = LaunchTinBot()
print(str_returnMsg)


#bot, str_returnMsg = LaunchTheiceBot()
#print(str_returnMsg)
#a = bot.driver.find_element_by_xpath('//*[@id="sessionNumber_chosen"]')
#a.send_keys('Afternoon Auction')








