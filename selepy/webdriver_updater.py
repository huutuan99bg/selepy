import shutil
from time import sleep, time
from tqdm import tqdm
from os.path import join, dirname
import os, sys
import requests
import zipfile
import pathlib
import re

class WebdriverUpdater:
    def __init__(self):
        """ 
        chromedriver_path
        """
        print('|\t'+self.emoji('heart')+'\tCS WebDriver\t'+self.emoji('success')+'\t|')
        self.home = str(pathlib.Path.home())
        self.cache_path = join(self.home, '.selepy_driver')
        self.chrome_path = self._get_chrome_path()
        self.chrome_version = self._get_chrome_version()
        if self.chrome_version == False:
            sys.exit('Chưa cài đặt trình duyệt chrome')
        compare_local = self.compare_local_version()
        if compare_local is True:
            self.chromedriver_path = join(self.cache_path, self.cache_chromedriver_version, 'chromedriver-win32', 'chromedriver.exe')
            print(self.emoji('success', 1)+self.emoji('time', 1)+'Chrome web driver load from cache, version '+self.cache_chromedriver_version)
        if compare_local is False or os.path.exists(self.chromedriver_path) is False:
            self.chromedriver_version = self._get_lastest_release()
            if self.compare_version(self.chromedriver_version['version'], self.chrome_version) is True:
                self.chromedriver_path = join(self.cache_path, self.chromedriver_version['version'], 'chromedriver-win32', 'chromedriver.exe')
                self.chromedriver_zip_path = join(self.cache_path, self.chromedriver_version['version'], 'chromedriver_win32.zip')
                self.chromedriver = self.get_chromedriver()
            else:
                sys.exit('Lỗi update chromedriver')

    def compare_version(self, version_1, version_2):
        try:
            if version_1.split('.')[0].strip() == version_2.split('.')[0].strip():
                return True
            else:
                return False
        except:
            return False

    def compare_local_version(self):
        try:
            with open(join(self.cache_path, 'version')) as f:
                self.cache_chromedriver_version = f.read()
        except:
            self.cache_chromedriver_version = 0
        try:
            cache_cd_ver = self.cache_chromedriver_version.split('.')[0].strip()
            cc_ver = self.chrome_version.split('.')[0].strip()
            if cache_cd_ver == cc_ver:
                return True
            else:
                return False
        except:
            return False
        
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
            url = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'
            res_json = requests.get(url).json()
            chromedrivers = res_json['channels']['Stable']['downloads']['chromedriver']
            chromedriver_win64 = list(filter(lambda c: c['platform'] == 'win32', chromedrivers))[0]['url']
            return {
                'url': chromedriver_win64, 
                'version' : res_json['channels']['Stable']['version']
            }
        except Exception as e:
            print('_get_lastest_release ERROR', e)
            return False
    def _download_file_progress_bar(self, url, filename, log = 'Download'):
        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            progress_bar = tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                bar_format=log+" {percentage:3.0f}%|{bar:15}| {n_fmt}B/{total_fmt}B ~ {rate_fmt} | {elapsed}<{remaining}",
            )
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    size = f.write(chunk)
                    progress_bar.update(size)
            progress_bar.close()
            return True
        except Exception as e:
            print('_download_file_progress_bar ERROR', e)
            return 
    def wirte_version(self):
        with open(join(self.cache_path, 'version'), 'w') as f:
            f.write(self.chromedriver_version['version'])
    # download the zip file using the url built above
    def _download_chromedriver(self):
        try:
            print(self.emoji('gear')+'Trying download chromedriver version '+self.chromedriver_version['version']+' from: '+self.chromedriver_version['url'])
            os.makedirs(dirname(self.chromedriver_zip_path), exist_ok=True)
            self._download_file_progress_bar(self.chromedriver_version['url'], self.chromedriver_zip_path, 'Download chromedriver')          

            with zipfile.ZipFile(self.chromedriver_zip_path, 'r') as zip_ref:
                zip_ref.extractall(dirname(dirname(self.chromedriver_path)))
            self.wirte_version()
            # print(self.emoji('success', 3)+'Donwload completed! Save file to cache: \n'+self.chromedriver_path)
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
                    if self.compare_version(p, self.chrome_version) is not True:
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
                print(self.emoji('success', 1)+self.emoji('time', 1)+'Chrome web driver load from cache, version '+self.chromedriver_version['version'])
                self.wirte_version()
                return self.chromedriver_path
            result = self._download_chromedriver()
            if result:
                print(self.emoji('success', 1)+self.emoji('time', 1)+'Download chromedriver time: '+str(round(time()-start_time, 2))+'s - Current version: '+self.chromedriver_version['version'])
                return self.chromedriver_path
            else:
                return False
        except Exception as e:
            print('get_chromedriver ERROR', e)
            return False