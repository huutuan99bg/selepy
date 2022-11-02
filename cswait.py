
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
class SWait:
    def __init__(self, driver):
        self.driver = driver
    # By Xpath 
    def get_element_by_xpath(self,limit_time,xpath):
        try:
            WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return self.driver.find_element(By.XPATH, xpath)
        except TimeoutException as exception: 
            return 'timeout'
    def get_elements_by_xpath(self,limit_time,xpath):
        try:
            WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return self.driver.find_elements(By.XPATH, xpath)
        except TimeoutException as exception: 
            return 'timeout'
    def click_by_xpath(self,limit_time,xpath):
        try:
            WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.XPATH, xpath))).click()
            return 'success'
        except TimeoutException as exception: 
            return 'timeout'
    def click_by_xpaths(self,limit_time,xpaths,time_wait = 1):
        try:
            count = 0
            while count < limit_time:
                for xpath in xpaths:
                    try:
                        print(count)
                        # self.driver.find_element_by_xpath(xpath).click()
                        WebDriverWait(self.driver, 0.1).until(EC.visibility_of_element_located((By.XPATH, xpath))).click()
                    except:
                        continue
                real_wait = time_wait - 0.1*len(xpaths)
                print('real wait: '+str(real_wait))
                sleep(real_wait)
                count = count + time_wait
            # WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.XPATH, xpath))).click()
            return 'success'
        except TimeoutException as exception: 
            return 'timeout'
    def send_keys_by_xpath(self,limit_time,xpath,text):
        try:
            WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(text)
            return 'success'
        except TimeoutException as exception: 
            return 'timeout'
    def get_attribute_by_xpath(self,limit_time,xpath,attribute):
        try:
            str = WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.XPATH, xpath))).get_attribute(attribute)
            return str if str != None else 'attribute_not_found'
        except TimeoutException as exception: 
            return 'timeout'
    def wait_until_by_xpath(self,limit_time,xpath):
        try:
            WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.XPATH,xpath)))
            return 'success'
        except TimeoutException as exception: 
            return 'timeout'
   
    # By Selector 
    def click_by_selector(self,limit_time,selector):
        try:
            WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).click()
            return 'success'
        except TimeoutException as exception: 
            return 'timeout'
    def find_by_selector(self,limit_time,selector):
        try:
            WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            return 'success'
        except TimeoutException as exception: 
            return 'timeout'
    def send_keys_by_selector(self,limit_time,selector,text):
        try:
            WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).send_keys(text)
            return 'success'
        except TimeoutException as exception: 
            return 'timeout'
    def get_attribute_by_selector(self,limit_time,selector,attribute):
        try:
            str = WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).get_attribute(attribute)
            return str if str != None else 'attribute_not_found'
        except TimeoutException as exception: 
            return 'timeout'
        
    # By ID 
    def click_by_id(self,limit_time,id):
        try:
            WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.ID, id))).click()
            return 'success'
        except TimeoutException as exception: 
            return 'timeout'
    def send_keys_by_id(self,limit_time,id,text):
        try:
            WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.ID, id))).send_keys(text)
            return 'success'
        except TimeoutException as exception: 
            return 'timeout'
    def get_attribute_by_id(self,limit_time,id,attribute):
        try:
            str = WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.ID, id))).get_attribute(attribute)
            return str if str != None else 'attribute_not_found'
        except TimeoutException as exception: 
            return 'timeout'
    def switch_to_frame_by_id(self,limit_time,id):
        try:
            WebDriverWait(self.driver, limit_time).until(EC.frame_to_be_available_and_switch_to_it((By.id,id)))
            return 'success'
        except TimeoutException as exception: 
            return 'timeout'
    def wait_until_by_xpath(self,limit_time,id):
        try:
            WebDriverWait(self.driver, limit_time).until(EC.visibility_of_element_located((By.ID,id)))
            return 'success'
        except TimeoutException as exception: 
            return 'timeout'
    # Go to nexttab
    def wait_nexttab(self, limit_time = 5):
        time = 0
        while time < limit_time:
            try:
                self.driver.switch_to.window(window_name= self.driver.window_handles[+1])
                return 'success'
            except:
                time = time+0.1
                continue
        return 'timeout'
    def wait_tab(self, tab, limit_time = 5):
        time = 0
        while time < limit_time:
            try:
                self.driver.switch_to.window(window_name= self.driver.window_handles[tab])
                return 'success'
            except:
                time = time+0.1
                continue
        return 'timeout'
         
    
    
        
