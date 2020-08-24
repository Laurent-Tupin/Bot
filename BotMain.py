import time
import pandas as pd
import fct_html as html


#==============================================================
# THEICE for Gold Price
#==============================================================
class c_botTheice(html.c_selenium_chrome):
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
class c_tinBot(html.c_selenium_chrome):
    def __init__(self):
        super().__init__(r'https://tinder.com')
        try:                        self.open()
        except Exception as err:    print('Error on Open Page || {}'.format(err))
        
    def loginFacebook(self, str_uid, str_pass):
        try:
            self.str_xPath = r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/header/div[1]/div[2]/div/button'
            self.clic('login', self.str_xPath)
            
            # Click to login facebook
            self.str_xPath = r'//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button'
            self.l_clickXPathIfFailed = [r'//*[@id="modal-manager"]/div/div/div/div/div[3]/span/button'
                                         ,r'//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[3]/button'] 
            self.clic('facebook', self.str_xPath, self.l_clickXPathIfFailed)
            # Login facebook
            self.changeWindow(1)
            self.fillUp(r'//*[@id="email"]', str_uid)
            self.fillUp(r'//*[@id="pass"]', str_pass)
            self.clic('', r'//*[@id="loginbutton"]', [])
            self.changeWindowBack()
            self.clearPopUpAfterId()
        except Exception as err:    
            print('Error on Login by Facebook || {}'.format(err))
            raise
        
    def clearPopUpAfterId(self):
        '''There is several possible Pop-Up we can encounter
        If the pop-up is not here, it will raise an error
        We dont want to handle the error as it is the normal behavior
        So we will just pass'''
        time.sleep(5)
        l_possiblePopUp = [r'//*[@id="content"]/div/div[2]/div/div/div[1]/button',
                           r'//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]',
                           r'//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]',
                           r'//*[@id="modal-manager"]/div/div/div[2]/button[1]',
                           r'//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]/span']
        for str_popUp in l_possiblePopUp:
            try:
                time.sleep(0.5)
                self.Clic(str_popUp)
            except: pass
        return True
    
    def like(self):
        time.sleep(1)
        self.str_likeButton = r'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button'
        self.clic('', self.str_likeButton, [])
        
    def closeMatchPopUp(self):
        time.sleep(1)
        self.str_closePopUpButton = r'//*[@id="modal-manager"]/div/div/div[2]/button[2]'
        self.str_closeMatchButton = r'//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a'
        try:
            self.clic('', self.str_closePopUpButton, [])
            print('Just closed Pop-up after {} LIKE'.format(str(self.i_like)))
        except:
            try:
                self.clic('', self.str_closeMatchButton, [])
                print('Just closed Match Pop-up after {} LIKE'.format(str(self.i_like)))
            except:
                print('We try to closeMatchPopUp by we cannot. Some popUp should be close before Like Loop')
                raise
        
    def likeLoop(self):
        time.sleep(30)
        self.i_compteur = 0
        self.i_like = 0
        for i in range(150):
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
    # Get Parameters
    str_path = r'C:\Users\Laurent.Tu\Documents\Apprendre Program\Python\Archive\Secret.csv'
    df_uid = pd.read_csv(str_path)
    str_uid = df_uid.loc[df_uid['Platform'] == 'facebook', 'Uid'].values[0]
    str_pass = df_uid.loc[df_uid['Platform'] == 'facebook', 'Password'].values[0]
    
    # Open Page
    bot = c_tinBot()
    # Login facebook
    bot.loginFacebook(str_uid, str_pass)
    # Like Loop
    try:        bot.likeLoop()
    except Exception as error: 
        print('ERROR Loop is over after {} LIKES and {} on the loop || {}'.format(str(bot.i_like), 
              str(bot.i_compteur), error))
        #bot.driver.close()
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








