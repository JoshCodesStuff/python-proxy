# python-proxy
A http proxy server I made for University, it downloads and caches html, images, anything requested through it.

## To Start the Proxy:
~~*You need Python 2 installed, it will not work with Python 3*~~
This program now solely works with Python3, and was written and tested with Python 3.9.
1. Navigate to the program's location in terminal
2. Run the program using `python3 Proxy.py [ip adress] [port]`, replacing the brackets with the corresponging info, see [ip address](https://en.wikipedia.org/wiki/IP_address) and [port](https://en.wikipedia.org/wiki/Port_(computer_networking)). For example: `python3 Proxy.py 127.0.0.1 8080` will host the server on port 8080 at your localhost address.
3. Run requests through the proxy to start caching.

Requests can be made using telnet, netcat, curl, wget and your web browser. I also built a CLI testing tool which, if run with the command `python3 -m Client -h` or `python3 Client.py -h` will provide usage details.

Mozilla has a guide [here](https://support.mozilla.org/en-US/kb/connection-settings-firefox?as=u&utm_source=inproduct) which allows you to add the proxy to the Firefox browser, enabling the usage of the tool. 

**REMINDER: This server will only run as an http server and may (will) not work with https requests.**
