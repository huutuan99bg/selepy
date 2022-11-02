import json
import os
import shutil
from os.path import join, dirname
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
try:
    from csmodules.cswait import SWait
except:
    from cswait import SWait
import requests
import zipfile
import pathlib
from selenium.webdriver.remote.command import Command
import re


class CSChromedriver:
    def __init__(self):
        print('|\t'+self.emoji('heart')+'\tCS WebDriver\t'+self.emoji('success')+'\t|')
        self.home = str(pathlib.Path.home())
        self.chrome_path = self.binary_path = self.get_chrome_path()
        self.chrome_version = self.get_chrome_version()
        if self.chrome_version == False:
            return False
        self.chromedriver_version = self.get_lastest_release()
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

    def get_chrome_path(self,):
        for item in map(os.environ.get, ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")):
            for subitem in (
                "Google/Chrome/Application",
                "Google/Chrome Beta/Application",
                "Google/Chrome Canary/Application",
            ):
                chrome_path = os.path.normpath(os.sep.join((item, subitem, "chrome.exe")))
                if os.path.exists(chrome_path):
                    return chrome_path

    def get_chrome_version(self):
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

    def get_lastest_release(self, ):
        try:
            url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_'+re.search("^\d+\.\d+\.\d+", self.chrome_version).group()
            response = requests.get(url)
            return response.text
        except:
            return False

    # download the zip file using the url built above
    def download_file(self):
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
            self.clear_old_versions()
            return True
        except:
            return False

    def clear_old_versions(self):
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
            result = self.download_file()
            if result:
                print(self.emoji('success', 1)+self.emoji('time', 1)+'Download chromedriver time: '+str(round(time()-start_time, 2))+'s - Current version: '+self.chromedriver_version)
                return self.chromedriver_path
            else:
                return False
        except:
            return False


csdriver = CSChromedriver()


def fix_chrome_crashed_alert(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        data['profile']['exit_type'] = "Normal"

        os.remove(path)
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
    except:
        return False


def open_driver(chrome_profile: str = None, proxy: str = None, binary_location: str = None, binary_auto: bool = True, images: bool = True, audio: bool = True, headless: bool = False, load_extensions: list = [], add_extensions: list = [],  incognito: bool = False, disable_webrtc: bool = False, chrome_agrs: list = [],):
    """
    Open chrome with selenium
    Args: 
        [chrome_profile]: str - path to chrome profile
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
        fix_chrome_crashed_alert(os.path.join(chrome_profile, r'Default\Preferences'))
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
        options.binary_location = csdriver.binary_path

    # Binary location
    if binary_location != None:
        options.binary_location = binary_location
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('useAutomationExtension', True)
    options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    if chrome_profile != None:
        options.add_argument("user-data-dir="+chrome_profile)
    options.add_argument("force-webrtc-ip-handling-policy")

    driver = webdriver.Chrome(csdriver.path, options=options)
    driver.implicitly_wait(2)
    cswait = SWait(driver)
    return (driver, cswait)
