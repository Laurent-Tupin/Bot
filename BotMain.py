# To use Chrome Driver
#  Go to chromedriver.chromium.org
#  download and UnZip the folder
#  Move it to Users/local/bin or C:\ProgramData\Anaconda3\Library\bin (Windows)


from selenium import webdriver

class TinderBot():
    def __init__(self, str_url):
        self.driver = webdriver.Chrome()
        self.driver.get(str_url)


str_url = r'https://tinder.com'
bot = TinderBot(str_url)


# Click



# Fill Out

