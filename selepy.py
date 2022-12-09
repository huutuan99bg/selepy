import requests
import zipfile
import pathlib
import re
import json
import os
import shutil
from os.path import join, dirname
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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

    def get_element_by_xpath(self, xpath, timeout = 5):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return self.find_element(By.XPATH, xpath)
        except TimeoutException as exception: 
            return False

    def get_elements_by_xpath(self, xpath, timeout = 5):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return self.find_elements(By.XPATH, xpath)
        except TimeoutException as exception: 
            return False

    def click_by_xpath(self, xpath, timeout = 5):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).click()
            return True
        except TimeoutException as exception: 
            return False

    def click_by_xpaths(self,xpaths:list,time_wait = 1, timeout = 5):
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

    def send_keys_by_xpath(self,xpath,text, timeout = 5):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(text)
            return True
        except TimeoutException as exception: 
            return False

    def get_attribute_by_xpath(self,xpath,attribute_name, timeout = 5):
        try:
            str = WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).get_attribute(attribute_name)
            return str if str != None else 'attribute_not_found'
        except TimeoutException as exception: 
            return False

    def wait_element_by_xpath(self, xpath, timeout = 5):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return True
        except:
            return False
   
    # By Selector 
    def click_by_selector(self,selector, timeout = 5):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).click()
            return True
        except TimeoutException as exception: 
            return False

    def find_by_selector(self,selector, timeout = 5):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            return True
        except TimeoutException as exception: 
            return False

    def send_keys_by_selector(self,selector,text, timeout = 5):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).send_keys(text)
            return True
        except TimeoutException as exception: 
            return False

    def get_attribute_by_selector(self,selector,attribute_name, timeout = 5):
        try:
            str = WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).get_attribute(attribute_name)
            return str if str != None else 'attribute_not_found'
        except TimeoutException as exception: 
            return False
        
    # By ID 
    def click_by_id(self,id, timeout = 5):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.ID, id))).click()
            return True
        except TimeoutException as exception: 
            return False

    def send_keys_by_id(self,id,text, timeout = 5):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.ID, id))).send_keys(text)
            return True
        except TimeoutException as exception: 
            return False

    def get_attribute_by_id(self,id,attribute, timeout = 5):
        try:
            str = WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.ID, id))).get_attribute(attribute)
            return str if str != None else 'attribute_not_found'
        except TimeoutException as exception: 
            return False

    def switch_to_frame_by_id(self,id, timeout = 5):
        try:
            WebDriverWait(self, timeout).until(EC.frame_to_be_available_and_switch_to_it((By.id,id)))
            return True
        except TimeoutException as exception: 
            return False
            
    def wait_element_by_id(self,id, timeout = 5):
        try:
            WebDriverWait(self, timeout).until(EC.visibility_of_element_located((By.ID,id)))
            return True
        except TimeoutException as exception: 
            return False
    # Go to nexttab
    def wait_next_tab(self, timeout = 5):
        time = 0
        while time < timeout:
            try:
                self.switch_to.window(window_name= self.window_handles[+1])
                return True
            except:
                time = time+0.1
                continue
        return False

    def wait_tab(self, tab_index, timeout = 5):
        time = 0
        while time < timeout:
            try:
                self.switch_to.window(window_name= self.window_handles[tab_index])
                return True
            except:
                time = time+0.1
                continue
        return False


class Selepy(CustomDriver):
    def __init__(self):
        print('|\t'+self.emoji('heart')+'\tCS WebDriver\t'+self.emoji('success')+'\t|')
        self.home = str(pathlib.Path.home())
        self.chrome_path = self.binary_path = self._get_chrome_path()
        self.chrome_version = self._get_chrome_version()
        if self.chrome_version == False:
            return False
        self.chromedriver_version = self._get_lastest_release()
        self.cache_path = join(self.home, 'cschromedriver')
        self.chromedriver_path = join(self.cache_path, self.chromedriver_version, 'chromedriver.exe')
        self.chromedriver_zip_path = join(self.cache_path, self.chromedriver_version, 'chromedriver_win32.zip')
        self.chromedriver = self.path = self.get_chromedriver()

    def emoji(self, option, quantity=1):
        output = ''
        emoji = ''
        if option == 'success':
            emoji = '\u2714\ufe0f '
        if option == 'heart':
            emoji = '\u2764\ufe0f '
        elif option == 'warning':
            emoji = '\u26A0\ufe0f '
        elif option == 'spicy':
            emoji = '\u1F336\ufe0f '
        elif option == 'time':
            emoji = '\u23F1\ufe0f '
        elif option == 'gear':
            emoji = '\u2699\ufe0f '
        for i in range(quantity):
            output += emoji
        return output

    def _get_chrome_path(self,):
        for item in map(os.environ.get, ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")):
            for subitem in (
                "Google/Chrome/Application",
                "Google/Chrome Beta/Application",
                "Google/Chrome Canary/Application",
            ):
                chrome_path = os.path.normpath(os.sep.join((item, subitem, "chrome.exe")))
                if os.path.exists(chrome_path):
                    return chrome_path

    def _get_chrome_version(self):
        ls = os.listdir(dirname(self.chrome_path))
        for p in ls:
            try:
                ver = re.search("^\d+\.\d+\.\d+\.\d+$", p).group()
                manifest_path = join(dirname(self.chrome_path), ver, ver + '.manifest')
                if ver != None and os.path.exists(manifest_path):
                    return ver
            except:
                pass
        return False

    def _get_lastest_release(self, ):
        try:
            url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_'+re.search("^\d+\.\d+\.\d+", self.chrome_version).group()
            response = requests.get(url)
            return response.text
        except:
            return False

    # download the zip file using the url built above
    def _download_chromedriver(self):
        try:
            url = "https://chromedriver.storage.googleapis.com/" + self.chromedriver_version + "/chromedriver_win32.zip"
            print(self.emoji('gear')+'Trying download chromedriver version '+self.chromedriver_version+' from: '+url)
            os.makedirs(dirname(self.chromedriver_zip_path), exist_ok=True)
            res = requests.get(url)
            open(self.chromedriver_zip_path, 'wb').write(res.content)
            with zipfile.ZipFile(self.chromedriver_zip_path, 'r') as zip_ref:
                zip_ref.extractall(dirname(self.chromedriver_path))
            print(self.emoji('success', 3)+'Donwload completed! Save file to cache: \n'+self.chromedriver_path)
            os.remove(self.chromedriver_zip_path)
            self._clear_old_versions()
            return True
        except:
            return False

    def _clear_old_versions(self):
        try:
            ls = os.listdir(self.cache_path)
            if len(ls) > 1:
                for p in ls:
                    if p != self.chromedriver_version:
                        shutil.rmtree(join(self.cache_path, p))
            return True
        except:
            return False

    def get_chromedriver(self):
        try:
            start_time = time()
            if self.chromedriver_version == False:
                return False
            if os.path.exists(self.chromedriver_path):
                print(self.emoji('success', 1)+self.emoji('time', 1)+'Chrome web driver load from cache, version '+self.chromedriver_version)
                return self.chromedriver_path
            result = self._download_chromedriver()
            if result:
                print(self.emoji('success', 1)+self.emoji('time', 1)+'Download chromedriver time: '+str(round(time()-start_time, 2))+'s - Current version: '+self.chromedriver_version)
                return self.chromedriver_path
            else:
                return False
        except:
            return False

    def _fix_chrome_crashed_alert(self, path):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            data['profile']['exit_type'] = "Normal"

            os.remove(path)
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)
        except:
            return False

    def _hook_remove_cdc_props(self):
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                    try {
                        let objectToInspect = window,
                        result = [];
                        while (objectToInspect !== null) {
                            result = result.concat(Object.getOwnPropertyNames(objectToInspect));
                            objectToInspect = Object.getPrototypeOf(objectToInspect);
                        }
                        result.forEach(p => {
                            p.match(/.+_.+_(Array|Promise|Symbol)/ig)
                                && delete window[p]
                        })
                        //console.log('Selepy bypass detect automation running!')
                    } catch (e) { }
                    """
            },
        )
        

    def open_driver(self, chrome_profile: str = None, proxy: str = None, binary_location: str = None, binary_auto: bool = True, images: bool = True, audio: bool = True, headless: bool = False, load_extensions: list = [], add_extensions: list = [],  incognito: bool = False, disable_webrtc: bool = False, chrome_agrs: list = [],):
        """
        Open chrome with selenium
        Args: 
            chrome_profile: str - path to chrome profile
            proxy: str(host:port) - set proxy to chrome 
            binary_location: str - path to chrome.exe location
            binary_auto: bool - auto check binary location
            images: bool - option enable/disable images
            audio: bool - option enable/disable audio
            headless: bool - option enable/disable headless
            load_extensions: list[str] - load unpacked extensions
            add_extensions: list[str] - add pack extensions
            incognito: bool - option open incognito mode
            disable_webrtc: bool - option disable/enable webrtc
            chrome_agrs: list[str] - more chrome arguments
        """
        if chrome_profile != None:
            self._fix_chrome_crashed_alert(os.path.join(chrome_profile, r'Default\Preferences'))
        options = Options()
        preferences = {}
        # WebRTC
        if disable_webrtc == True:
            preferences = {
                "webrtc.ip_handling_policy": "disable_non_proxied_udp",
                "webrtc.multiple_routes_enabled": False,
                "webrtc.nonproxied_udp_enabled": False,
                "enforce-webrtc-ip-permission-check": True
            }

        # Images
        img_option = 1 if images == True else 2
        preferences["profile.managed_default_content_settings.images"] = img_option
        options.add_experimental_option("prefs", preferences)

        if headless == True:
            options.add_argument('--headless')

        # Proxy
        if proxy != None:
            proxy_server = '--proxy-server=http://'+str(proxy)
            options.add_argument(proxy_server)
        # audio
        if audio == False:
            options.add_argument("--mute-audio")
        if incognito == True:
            options.add_argument('--incognito')
        # Another arguments
        if len(chrome_agrs) > 0:
            for agr in chrome_agrs:
                options.add_argument(agr)
        # Add extensions
        if len(add_extensions) > 0:
            for ext in add_extensions:
                options.add_extension(ext)
        # Load extensions
        if len(load_extensions) > 0:
            exts = '--load-extension='
            for ext in load_extensions:
                exts += ext+','
            options.add_argument(exts)
        # Binary auto
        if binary_auto == True and binary_location is None:
            options.binary_location = self.binary_path

        # Binary location
        if binary_location != None:
            options.binary_location = binary_location
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('useAutomationExtension', True)
        options.add_argument('--no-sandbox')
        options.add_argument('--lang=en')

        # options.add_argument('--disable-dev-shm-usage')
        if chrome_profile != None:
            options.add_argument("user-data-dir="+chrome_profile)
        options.add_argument("force-webrtc-ip-handling-policy")
        # self.driver = webdriver.Chrome(self.chromedriver, options=options)
        self.driver = CustomDriver(self.chromedriver, options=options)
        self.driver.implicitly_wait(2)
        self._hook_remove_cdc_props()
        return self.driver
