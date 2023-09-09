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

setProxyTask('163.172.174.138', '10798', proxy_username = 'b47521f3e1e0a9587c3c196f0497c696', proxy_password = '_JTItIEll9LD6Lzi');