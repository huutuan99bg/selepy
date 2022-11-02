# Selepy - website testing tool base on selenium
Docs: coming soon

# Example:
```python
proxy = '192.168.0.103:'+str(port)
# proxy = '127.0.0.1:1080'
print('Open chrome')
(driver,cswait) = Selepy().open_driver(chrome_profile= chrome_path,proxy= proxy,images=True, binary_auto= True, incognito=False, )
```
