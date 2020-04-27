import pandas as pd 
import time
import re
import requests
from bs4 import BeautifulSoup
import unicodedata


def Act_WaitTranslation(int_sec = 5):
    print('  * Wait for Translation {} secondes ...'.format(str(int_sec)))
    time.sleep(int_sec)

def fBl_ChineseInString(str_stringToTest):
    l_result = re.findall(r'[\u4e00-\u9fff]+', str_stringToTest)
    if l_result:    return True
    return False


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


