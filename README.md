# Selepy - website testing tool base on selenium
# Documents
Automate google chrome with selenium<br />
Args: <br />
    chrome_profile: str - path to chrome profile<br />
    proxy: str(host:port) - set proxy to chrome <br />
    binary_location: str - path to chrome.exe location<br />
    binary_auto: bool - auto check binary location<br />
    images: bool - option enable/disable images<br />
    audio: bool - option enable/disable audio<br />
    headless: bool - option enable/disable headless<br />
    load_extensions: list[str] - load unpacked extensions<br />
    add_extensions: list[str] - add pack extensions<br />
    incognito: bool - option open incognito mode<br />
    disable_webrtc: bool - option disable/enable webrtc<br />
    chrome_agrs: list[str] - more chrome arguments<br />

# Example:
```python
chrome_path = r'E:\ChromePortable\Data\profile'
proxy = '192.168.0.103:4020'
print('Open chrome')
(driver,cswait) = Selepy().open_driver(chrome_profile= chrome_path,proxy= proxy, images=False,)
```
