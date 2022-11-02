# Selepy - website testing tool base on selenium
# Documents
Automate google chrome with selenium
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

# Example:
```python
chrome_path = r'E:\ChromePortable\Data\profile'
proxy = '192.168.0.103:4020'
print('Open chrome')
(driver,cswait) = Selepy().open_driver(chrome_profile= chrome_path,proxy= proxy, images=False,)
```
