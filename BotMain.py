import time
import pandas as pd
import fct_html as html


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
        except:     print('Error on I accept cookies')
        time.sleep(30)
        try:        super().clic('', r'//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]', [])
        except:     print('Error on 1 ALLOW Location')
        try:        super().clic('', r'//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]', [])
        except:     print('Error on 2 Enable Notifications')
        try:        super().clic('', r'//*[@id="modal-manager"]/div/div/div[2]/button[1]', [])
        except:     print('Error on 3')
        
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
            self.i_compteur = i
            try:
                self.like()
                self.i_like += 1
            except:
                self.closeMatchPopUp()
        print('Loop is over successfully after {} LIKES and {} on the compteur'.format(str(self.i_like), str(self.i_compteur)))


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
    try:    bot.likeLoop()
    except: print('ERROR Loop is over after {} LIKES and {} on the compteur'.format(str(bot.i_like), str(bot.i_compteur)))
    
    return bot, 'END'

bot, str_returnMsg = LaunchTinBot()
print(str_returnMsg)
    
    
