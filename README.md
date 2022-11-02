# Selepy - website testing tool base on selenium
# Documents
Automate google chrome with selenium<br />
Args: <br />
__chrome_profile: str - path to chrome profile<br />
__proxy: str(host:port) - set proxy to chrome <br />
__binary_location: str - path to chrome.exe location<br />
__binary_auto: bool - auto check binary location<br />
__images: bool - option enable/disable images<br />
__audio: bool - option enable/disable audio<br />
__headless: bool - option enable/disable headless<br />
__load_extensions: list[str] - load unpacked extensions<br />
__add_extensions: list[str] - add pack extensions<br />
__incognito: bool - option open incognito mode<br />
__disable_webrtc: bool - option disable/enable webrtc<br />
__chrome_agrs: list[str] - more chrome arguments<br />

# Example:
```python
chrome_path = r'E:\ChromePortable\Data\profile'
proxy = '192.168.0.103:4020'
print('Open chrome')
(driver,cswait) = Selepy().open_driver(chrome_profile= chrome_path,proxy= proxy, images=False,)
```
