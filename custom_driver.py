from random import randint
from time import sleep, time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class CustomDriver(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        webdriver.Chrome.__init__(self, *args, **kwargs)

    def execute_first_script(self, script):
        try:
            self.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": script
                },
            )
        except Exception as e:
            print(e)
            return False

    def close_another(self):
        try:
            current_window = self.current_window_handle
            for w in self.window_handles:
                if w != current_window:
                    self.switch_to.window(w)
                    self.close()
            self.switch_to.window(current_window)
            return True
        except Exception as e:
            print(e)
            return False

    def execute_first_script_from_file(self, script_path):
        try:
            script =open(script_path, "r").read()
            self.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": script
                },
            )
            return True
        except Exception as e:
            print(e)
            return False

    def execute_script_from_file(self, script_path):
        try:
            script =open(script_path, "r").read()
            self.execute_script(script)
            return True
        except Exception as e:
            print(e)
            return False

    def get_element_by_xpath(self, xpath, timeout = 10):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return self.find_element(By.XPATH, xpath)
        except TimeoutException as exception: 
            return False

    def get_elements_by_xpath(self, xpath, timeout = 10):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return self.find_elements(By.XPATH, xpath)
        except TimeoutException as exception: 
            return False

    def click_by_xpath(self, xpath, timeout = 10):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).click()
            return True
        except TimeoutException as exception: 
            return False

    def click_by_xpaths(self,xpaths:list,time_wait = 1, timeout = 10):
        try:
            count = 0
            while count < timeout:
                for xpath in xpaths:
                    try:
                        WebDriverWait(self, 0.1).until(EC.visibility_of_element_located((By.XPATH, xpath))).click()
                    except:
                        continue
                real_wait = time_wait - 0.1*len(xpaths)
                print('real wait: '+str(real_wait))
                sleep(real_wait)
                count = count + time_wait
            return True
        except TimeoutException as exception: 
            return False

    def simulator_send_keys(self, element, text):
        for char in text:
            element.send_keys(char)
            sleep(randint(40, 120) * 0.001)

    def send_keys_by_xpath(self,xpath, text, timeout = 10, simulator = False):
        try:
            element = WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            if simulator is False:
                element.send_keys(text)
            else:
                for char in text:
                    element.send_keys(char)
                    sleep(randint(40, 120) * 0.001)
            return True
        except TimeoutException as exception: 
            return False

    def get_attribute_by_xpath(self,xpath,attribute_name, timeout = 10):
        try:
            str = WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).get_attribute(attribute_name)
            return str if str != None else 'attribute_not_found'
        except TimeoutException as exception: 
            return False

    def wait_element_by_xpath(self, xpath, timeout = 10):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return True
        except:
            return False
   
    # By Selector 
    def click_by_selector(self,selector, timeout = 10):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).click()
            return True
        except TimeoutException as exception: 
            return False

    def find_by_selector(self,selector, timeout = 10):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            return True
        except TimeoutException as exception: 
            return False

    def send_keys_by_selector(self,selector,text, timeout = 10, simulator = False):
        try:
            element = WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            if simulator is False:
                element.send_keys(text)
            else:
                for char in text:
                    element.send_keys(char)
                    sleep(randint(40, 120) * 0.001)
            return True
        except TimeoutException as exception: 
            return False

    def get_attribute_by_selector(self,selector,attribute_name, timeout = 10):
        try:
            str = WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).get_attribute(attribute_name)
            return str if str != None else 'attribute_not_found'
        except TimeoutException as exception: 
            return False
        
    # By ID 
    def click_by_id(self,id, timeout = 10):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.ID, id))).click()
            return True
        except TimeoutException as exception: 
            return False

    def send_keys_by_id(self,id,text, timeout = 10, simulator = False):
        try:
            element = WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.ID, id)))
            if simulator is False:
                element.send_keys(text)
            else:
                for char in text:
                    element.send_keys(char)
                    sleep(randint(40, 120) * 0.001)
            return True
        except TimeoutException as exception: 
            return False

    def get_attribute_by_id(self,id,attribute, timeout = 10):
        try:
            str = WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.ID, id))).get_attribute(attribute)
            return str if str != None else 'attribute_not_found'
        except TimeoutException as exception: 
            return False

    def switch_to_frame_by_id(self, id, timeout = 10):
        try:
            WebDriverWait(self, timeout).until(EC.frame_to_be_available_and_switch_to_it((By.id,id)))
            return True
        except TimeoutException as exception: 
            return False
            
    def wait_element_by_id(self,id, timeout = 10):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.ID,id)))
            return True
        except TimeoutException as exception: 
            return False
    # Go to nexttab
    def wait_next_tab(self, timeout = 10):
        time = 0
        while time < timeout:
            try:
                self.switch_to.window(window_name= self.window_handles[+1])
                return True
            except:
                time = time+0.1
                continue
        return False

    def wait_tab(self, tab_index, timeout = 10):
        time = 0
        while time < timeout:
            try:
                self.switch_to.window(window_name= self.window_handles[tab_index])
                return True
            except:
                time = time+0.1
                continue
        return False
    
    def quit_tabs(self):
        start_close = time()
        try:
            for window_handle in self.window_handles:
                self.switch_to.window(window_name=self.window_handles[0])
                self.close()
            # print('Close completed - '+str(round(time()-start_close, 2))+'s')
        except Exception as e:
            return False
        
    def quit_tabs_in_thread(self):
        Thread(target=self.quit_tabs,).start()