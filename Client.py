#!/usr/bin/env python3
""" Exists only to test the Proxy.py module

    Run this with the command 'python Client.py' and it will
    download www.testingmcafeesites.com/testcat_ac.html from
    its hosted server. Change the URL on line 28 if needed
"""
import socket
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect to http proxy server and pass requests.")
    parser.add_argument('-u','--url', 
        help="format: http://example.com",
        default="http://www.testingmcafeesites.com/testcat_ac.html",
        type=str)

    parser.add_argument('-t','--type',
        help="select request type from [GET,HEAD,DELETE]",
        choices=["GET",
                "HEAD",
                "DELETE",],
        default="GET")

    parser.add_argument('--hostname',
        help="specify hostname details. Defaults to localhost.",
        default='localhost')

    parser.add_argument('--port',
        help="specify the server port number. Defaults to 8080.",
        default=8080,
        type=int)

    args = parser.parse_args()

    # 1MB buffer size
    BUFFER_SIZE = 1048576

    #create the client socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #try to connect to the server
    print('attempting to connect to server')
    try:
        clientSocket.connect((args.hostname,args.port))
        print('connection successful')
    except:
        print('could not connect to proxy')

    
    request = f'{args.t} {args.url} HTTP/1.1'   # form request
    request_as_bytes = str.encode(request)      # encode request as bytes object for transport

    print('attempting to send request')
    try:
        clientSocket.send(request_as_bytes)
    except:
        print('failed to send')

    #receive results from request
    try:
        result = (clientSocket.recv(BUFFER_SIZE)).decode('utf-8')
    except:
        print('received no response from server')

    print('Result of request - ' + '\n' + result)
    clientSocket.close()