import pandas as pd 
import time
import re
import requests
from bs4 import BeautifulSoup
import unicodedata
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


#------------------------------------------------------------------------------
# Check Connexion
#------------------------------------------------------------------------------
def fBL_checkConnexion(o_page):
    try: 
        if o_page.status_code == 200: 
            return True
        else: 
            print(' Connexion close for the status code of the page is not 200 ' )
            print(' - Status code of the page is: ' + o_page.status_code)
    except: 
        print('  ERROR in fBL_checkConnexion: Connexion fails because the input is not a page')
    return False


#------------------------------------------------------------------------------
# Function to check parameters
#------------------------------------------------------------------------------
def Act_WaitTranslation(int_sec = 5):
    print('  * Wait for Translation {} secondes ...'.format(str(int_sec)))
    time.sleep(int_sec)

def fBl_ChineseInString(str_stringToTest):
    l_result = re.findall(r'[\u4e00-\u9fff]+', str_stringToTest)
    if l_result:    return True
    return False




#------------------------------------------------------------------------------
# Entrance/Main Function
#------------------------------------------------------------------------------
def fDf_htmlGetArray_json(str_url, str_jsonCriteria = ""):
    try:
        o_page = requests.get(str_url)
    except:
        print(' ERROR in fDf_htmlGetArray_json: requests.get(str_url)')
        print(' - ', str_url)
        raise
    if not fBL_checkConnexion(o_page): 
        print(' ERROR in fDf_htmlGetArray_json: fBL_checkConnexion')
        print('  - URL in fDf_htmlGetArray_json is: ', str_url)
        return False
    #print(o_page.content)
    try:
        df = pd.DataFrame(o_page.json()[str_jsonCriteria])
    except:
        print(' ERROR in fDf_htmlGetArray_json: pd.DataFrame(o_page.json()[str_jsonCriteria])')
        print(' - ', str_url)
        print(' - ', str_jsonCriteria)
        raise
    return df


def fDf_htmlGetArray_Soup(str_url, bl_th = False, bl_waitForTranslation = False, int_waitTime = 1, bl_cleanXA0 = True):  
    arr_result = []
    try:
        d_headers = {'User-Agent': 'Chrome/71.0.3578.98'}     #Chrome/71.0.3578.98      #Mozilla/5.0
        o_page = requests.get(str_url, headers = d_headers)
        if bl_waitForTranslation:       Act_WaitTranslation(int_waitTime)
    except:
        print(' ERROR in fDf_htmlGetArray_Soup: requests.get(str_url)')
        print(' -  ', str_url)
        raise
    if not fBL_checkConnexion(o_page): 
        print(' ERROR in fDf_htmlGetArray_Soup: fBL_checkConnexion(o_page): ')
        print(' -  ', str_url)
        return False    
    try:
        bs_soup = BeautifulSoup(o_page.content, "html.parser")
    except:
        print(' ERROR in fDf_htmlGetArray_Soup: BeautifulSoup(o_page.content, "html.parser")')
        print(' -  ', str_url)
        raise
    try:
        for o_table in bs_soup.find_all('table'):
            for o_row in o_table.find_all('tr'):
                # Balise Th = Text / Titre
                o_th = [o_cell.text.strip() for o_cell in o_row.find_all('th')]                
                if bl_th and o_th:      o_cells = o_th
                else:                   o_cells = []
                # Balise TD = Chiffre
                o_td = [o_cell.text.strip() for o_cell in o_row.find_all('td')]
                if o_td:                o_cells = o_cells + o_td
                elif o_th:              o_cells = o_th
                else:                   o_cells = []    
                # Clean Cells
                if bl_cleanXA0:
                    o_cells = [unicodedata.normalize("NFKD",cel_Text) for cel_Text in o_cells]
                    o_cells = [cel_Text.replace('\n', '  ').replace('\r', '') for cel_Text in o_cells]
                # add the row to result
                if o_cells:   arr_result.append(o_cells)
                # Chinese Translation - Recursive                
                if bl_waitForTranslation:
                    for cell in o_cells:
                        if fBl_ChineseInString(cell):
                            if int_waitTime > 60:
                                print('   *_* ERROR : still Chinese within Result: ', cell)
                                print('   *_!!!_* Cannot wait anymore, Do it manually: ')
                                print('   *_URL_* ', str_url)
                                break
                            elif int_waitTime > 20:     int_waitTime = int_waitTime + 20
                            elif int_waitTime > 10:     int_waitTime = int_waitTime + 10
                            else:                       int_waitTime = int_waitTime + 5
                            print('   *_* ERROR : still Chinese in Result: ', cell)
                            df_return = fDf_htmlGetArray_Soup(str_url, bl_th, True, int_waitTime)
                            return df_return
        df = pd.DataFrame(arr_result)
    except:
        print(' ERROR in fDf_htmlGetArray_Soup: LOOP on tables / rows / cells')
        print(' -  ', str_url)
        raise
    return df



#------------------------------------------------------------------------------
# Class Selenium
#------------------------------------------------------------------------------
class c_selenium_chrome():
    # ----------------------------------------------------
    # To use Chrome Driver
    #  https://chromedriver.chromium.org/
    #  download and UnZip the folder
    #  Move it to Users/local/bin or C:\ProgramData\Anaconda3\Library\bin (Windows)
    # ----------------------------------------------------
    def __init__(self, str_url):
        self.driver = selenium.webdriver.Chrome()
        self.str_url = str_url
    
    def open(self):
        self.driver.get(self.str_url)
    
    def clic(self, str_buttonName, str_buttonxPath, l_buttonIfFailed):
        # ----------------------------------------------------
        # Right click on the button and chose Inspect
        # Spot the button Type
        # Right Click and Copy XPath, You get the XPATH
        # ----------------------------------------------------
        time.sleep(5)
        btn_click = self.driver.find_element_by_xpath(str_buttonxPath)
        if str_buttonName.lower() in btn_click.text.lower():
            btn_click.click()
        else:
            print('Link found was not {} but: {}'.format(str_buttonName, btn_click.text))
            for xPath in l_buttonIfFailed:
                time.sleep(5)
                btn_click = self.driver.find_element_by_xpath(xPath)
                print('Link is: {}'.format(btn_click.text))
                btn_click.click() 
    
    def fillUp(self, str_buttonxPath, str_textToFill):
        time.sleep(5)
        Area_toFill = self.driver.find_element_by_xpath(str_buttonxPath)
        Area_toFill.send_keys(str_textToFill)
    
    def changeWindow(self, int_nbWindow):
        self.baseWindow = self.driver.window_handles[0]
        self.int_nbWindowsTotal = len(self.driver.window_handles)
        int_nbWindow = int_nbWindow % self.int_nbWindowsTotal
        self.newWindow = self.driver.window_handles[int_nbWindow]
        self.driver.switch_to.window(self.newWindow)
        
    def changeWindowBack(self):
        try:        self.driver.switch_to.window(self.baseWindow)
        except:
            print('Could not go back to Base Window... Wron use of changeWindowBack... Make sure u used changeWindow before')
            self.driver.switch_to.window(self.driver.window_handles[0])
    
    def clicCaptcha(self, str_recaptcha):
        self.str_recaptcha = str_recaptcha
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,
                     "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.str_recaptcha))).click()
        


