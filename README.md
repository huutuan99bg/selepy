# Selepy - website testing tool base on selenium
# Documents
Automate google chrome with selenium\
Features: Bypass cloudflare, fix some bugs of selenium core, and many other features...\
Args: \
&emsp;&emsp;chrome_profile: str - path to chrome profile<br />
&emsp;&emsp;proxy: str(host:port) - set proxy to chrome <br />
&emsp;&emsp;binary_location: str - path to chrome.exe location<br />
&emsp;&emsp;binary_auto: bool - auto check binary location<br />
&emsp;&emsp;images: bool - option enable/disable images<br />
&emsp;&emsp;audio: bool - option enable/disable audio<br />
&emsp;&emsp;headless: bool - option enable/disable headless<br />
&emsp;&emsp;load_extensions: list[str] - load unpacked extensions<br />
&emsp;&emsp;add_extensions: list[str] - add pack extensions<br />
&emsp;&emsp;incognito: bool - option open incognito mode<br />
&emsp;&emsp;disable_webrtc: bool - option disable/enable webrtc<br />
&emsp;&emsp;chrome_agrs: list[str] - more chrome arguments<br />

# Example:
```python
chrome_path = r'E:\ChromePortable\Data\profile'
proxy = '192.168.0.103:4020'
print('Open chrome')
driver = Selepy().open_driver(chrome_profile= chrome_path,proxy= proxy, images=False,)
```
