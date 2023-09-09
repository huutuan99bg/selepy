#%%
import tempfile
import shutil
import json

def generate_ext_proxy(proxy_host, proxy_port, proxy_username, proxy_password):
    temp_dir = tempfile.mkdtemp(prefix='extension_proxy_')
    manifest_data = {
        "background": {
            "scripts": [
                "proxy.js"
            ]
        },
        "manifest_version": 2,
        "name": "Mr.T Proxy",
        "short_name": "mrt_proxy",
        "permissions": [
            "proxy",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking",
            "*://*/*"
        ],
        "version": "0.0.1"
    }

    background_code = """
    const setProxyTask = (proxy_host, proxy_port, proxy_username = null, proxy_password = null) => {
        var config = {
            mode: "pac_script",
            pacScript: {
                data: `function FindProxyForURL(url, host) {
                        if (shExpMatch(host, "*.jpg") || host.match(/myip.com/)){
                            return 'DIRECT';
                        }else{
                            return 'PROXY ${proxy_host}:${proxy_port}';
                        }
                    }`
            }
        };
        chrome.proxy.settings.set({ value: config, scope: "regular" }, function () { });
        function callbackAuthProxy(details) {
            return {
                authCredentials: {
                    username: proxy_username,
                    password: proxy_password
                }
            };
        }
        if (proxy_username != null && proxy_password != null) {
            chrome.webRequest.onAuthRequired.addListener(
                callbackAuthProxy,
                { urls: ["<all_urls>"] },
                ['blocking']
            );
        }

    }

    """
    if proxy_username is None: proxy_username = 'null'
    if proxy_password is None: proxy_password = 'null'
    background_code += f"setProxyTask('{proxy_host}', '{proxy_port}', proxy_username = '{proxy_username}', proxy_password = '{proxy_password}');"

    manifest_path = f"{temp_dir}/manifest.json"
    with open(manifest_path, "w") as manifest_file:
        manifest_file.write(json.dumps(manifest_data))

    background_path = f"{temp_dir}/proxy.js"
    with open(background_path, "w") as background_file:
        background_file.write(background_code)

    return temp_dir

# generate_ext_proxy('163.172.174.138','10798','b47521f3e1e0a9587c3c196f0497c696','_JTItIEll9LD6Lzi')
