#%%
import json
import os, sys
from os.path import join, dirname
from time import sleep, time
import uuid
import subprocess
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# Custom modules
curdir = dirname(__file__)
sys.path.append(curdir)
from custom_driver import CustomDriver
from webdriver_updater import WebdriverUpdater
from extension_proxy import generate_ext_proxy
webdriver_updater = WebdriverUpdater()

# Remover
remover_path = join(curdir, 'remover.py')
temp_folder = join(curdir, 'temp_profiles')
this_pid = os.getpid()
os.makedirs(temp_folder, exist_ok=True)
remover_process = subprocess.Popen(['python', remover_path, temp_folder, str(this_pid)], creationflags=subprocess.DETACHED_PROCESS)

class Selepy(CustomDriver):
    def __init__(self):
        self.chromedriver = webdriver_updater.chromedriver_path
        self.chrome_path = webdriver_updater.chrome_path
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
        

    def open_driver(self, chrome_profile: str = None, proxy: str = None, ext_proxy = None, binary_location: str = None, binary_auto: bool = True, images: bool = True, audio: bool = True, headless: bool = False, load_extensions: list = [], add_extensions: list = [],  incognito: bool = False, disable_webrtc: bool = False, chrome_agrs: list = [], rect: tuple = (), disable_password = True):
        """
        Open chrome with selenium
        Args: 
            chrome_profile: str - path to chrome profile
            proxy: str(host:port) - set proxy to chrome 
            ext_proxy: json - host, port, username, password - Set proxy using extension, and authentication
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
            rect: tuple - (top, left, width, height) - Position and site of browser
        """
        if chrome_profile is not None:
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
        preferences["profile.default_content_setting_values.notifications"] = 2
        if disable_password == True:
            preferences["credentials_enable_service"] = False
            preferences["profile.password_manager_enabled"] = False
        options.add_experimental_option("prefs", preferences)

        if headless == True:
            options.add_argument('--headless')

        # Extension proxy
        
        if ext_proxy is not None:
            try:
                extension_proxy_path = generate_ext_proxy(ext_proxy['host'], ext_proxy['port'], ext_proxy.get('username'), ext_proxy.get('password'))
                load_extensions.append(extension_proxy_path)
            except Exception as e:
                raise Exception('Set ext proxy ERROR', e)
        # Proxy
        elif proxy != None:
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
            options.binary_location = self.chrome_path 

        # Rect
        if len(rect) > 0:
            if len(rect) != 4:
                print('!!!!! Argument rect not valid, (top, left, width, height)')
            else:
                # print('Set size and position', rect)
                options.add_argument(f'--window-position={rect[1]},{rect[0]}')
                options.add_argument(f'--window-size={rect[2]},{rect[3]}')

        # Binary location
        if binary_location != None:
            options.binary_location = binary_location
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('useAutomationExtension', True)
        options.add_argument('--no-sandbox')
        options.add_argument('--lang=en')
        # Disable logging
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--output=/dev/null")
        
        # options.add_argument('--disable-dev-shm-usage')
        if chrome_profile is None:
            profile_name = 'chrome__'+uuid.uuid4().hex[:16]
            chrome_profile = join(temp_folder, profile_name)
        options.add_argument("user-data-dir="+chrome_profile)

        options.add_argument("force-webrtc-ip-handling-policy")
        # self.driver = webdriver.Chrome(self.chromedriver, options=options)
        service = Service(self.chromedriver)
        self.driver = CustomDriver(service=service, options=options)
        self.driver.implicitly_wait(2)
        self._hook_remove_cdc_props()
        return self.driver

# ext_proxy = {
#     'host': '51.159.149.198',
#     'port': 10798,
#     'username': 'b47521f3e1e0a9587c3c196f0497c696',
#     'password': '_JTItIEll9LD6Lzi'
# }
# driver = Selepy().open_driver(ext_proxy = ext_proxy, audio=False)
# driver.get('https://whoer.net')
# sleep(999)