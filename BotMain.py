import time
import pandas as pd
import fct_html as html


def LaunchTinderBot():
    # Open Page
    try:
        str_url = r'https://tinder.com'
        bot = html.c_Selenium_InteractInternet(str_url)
    except: return 'Error on Open Page'
        
    # Click to login facebook
    try:
        str_xPath = r'//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button'
        l_clickXPathIfFailed = [r'//*[@id="modal-manager"]/div/div/div/div/div[3]/span/button'
                                ,r'//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[3]/button']                        
        bot.clic('facebook', str_xPath, l_clickXPathIfFailed)
    except: return 'Error on Click to login facebook'
        
    # Login facebook
    try:
        bot.changeWindow(1)
        str_path = r'C:\Users\Laurent.Tu\Documents\Apprendre Program\Python\Archive\Secret.csv'
        df_uid = pd.read_csv(str_path)
        str_uid = df_uid.loc[df_uid['Platform'] == 'facebook', 'Uid'].values[0]
        str_pass = df_uid.loc[df_uid['Platform'] == 'facebook', 'Password'].values[0]
        bot.fillUp(r'//*[@id="email"]', str_uid)        
        bot.fillUp(r'//*[@id="pass"]', str_pass)
        bot.clic('', r'//*[@id="loginbutton"]', [])
        bot.changeWindowBack()
    except: return 'Error on login facebook'
        
    # pop-Up
    time.sleep(10)
    try:        bot.clic('', r'//*[@id="content"]/div/div[2]/div/div/div[1]/button', [])
    except:     print('Error on I accept cookies')
    time.sleep(50)
    try:        bot.clic('', r'//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]', [])
    except:     print('Error on 1')
    try:        bot.clic('', r'//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]', [])
    except:     print('Error on 2')
    try:        bot.clic('', r'//*[@id="modal-manager"]/div/div/div[2]/button[1]', [])
    except:     print('Error on 3')
        
    # LIKE in a Loop
    try:
        i_compteur = 0
        str_likeButton = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[3]'
        str_closePopUpButton = '//*[@id="modal-manager"]/div/div/div[2]/button[2]'
        str_closeMatchButton = '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a'
        for i_compteur in range(10000):
            time.sleep(1)
            try:        bot.clic(str_likeButton)
            except:
                time.sleep(1)
                try:    bot.clic(str_closePopUpButton)
                except: bot.clic(str_closeMatchButton)
    except: return 'Error on LIKE in a Loop after {} profiles'.format(str(i_compteur))
    return 'LIKE on {} profiles'.format(str(i_compteur))


v_TinderBot = LaunchTinderBot()
print(v_TinderBot)
    
    
