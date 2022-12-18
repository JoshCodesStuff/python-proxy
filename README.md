# python-proxy
A http proxy server I made for University, it downloads and caches html, images, anything requested through it.

## To Start the Proxy:
~~*You need Python 2 installed, it will not work with Python 3*~~
1. Navigate to the code location in terminal
2. Run the code using `python3 Proxy.py [ip adress] [port]`, replacing the brackets with the corresponging info, see [ip address](https://en.wikipedia.org/wiki/IP_address) and [port](https://en.wikipedia.org/wiki/Port_(computer_networking)). For example: `python3 Proxy.py 127.0.0.1 8080` will host the server on port 8080 at your localhost address.
3. Run requests through the proxy to start caching.

Requests can be run through using telnet, netcat, curl, wget and your web browser. This allows you to add it as a proxy for Firefox using their guide found [here](https://support.mozilla.org/en-US/kb/connection-settings-firefox?as=u&utm_source=inproduct).

**This server will only run as an http server and may (will) not work with https requests.**
