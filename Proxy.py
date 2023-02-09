#!/usr/bin/env python3
""" A program which uses http to download files over the internet and cache them.
    Author: Josh Codes
    Github: https://github.com/JoshCodesStuff
"""

# Include the libraries for socket and system calls
import socket
import sys
import os
import argparse
import re

# 1MB buffer size
BUFFER_SIZE = 1048576

if __name__ == "__main__":
    # parse command line arguments for later use
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname', help='the IP Address Of Proxy Server')
    parser.add_argument('port', help='the port number of the proxy server')
    args = parser.parse_args()

    # use command line arguments as hostname &| portname
    host = args.hostname
    port = int(args.port)

    try:
        # create the socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Created Socket")
    except:
        sys.exit("Failed to create socket")

    try:
        #bind the server socket to a host and port
        serversocket.bind((host,port))
        print("Port is bound successfully")
    except:
        sys.exit("Port is already in use")

    try:
        # listen on the server socket
        serversocket.listen(12) # might change this for simultaneous
        print("Listening to socket")
    except:
        sys.exit("Failed to listen")
    
    # processing loop of function
    while True:
        print("Waiting for connection")

        clientSocket = None

        try:
            # Accept connection from client and stor in the clientSocket
            (clientSocket,address) = serversocket.accept()
            print("Received a connection from: " + args.hostname)
        except:
            sys.exit("Failed to accept connection")
        
        message = "METHOD URI VERSION"

        # Get request from client and store in message
        message = clientSocket.recv(BUFFER_SIZE)
        print(f"Received request:\n<{message.decode()}")
        requestParts = message.split()
        
        method  = requestParts[0].decode()
        uri     = requestParts[1].decode()
        version    = requestParts[2].decode()

        print(f"Method:\t\t {method}")
        print(f"URI:\t\t {uri}")
        print(f"Version:\t {version}\n")

        uri = re.sub('^(/?)http(s?)://', '', uri, 1)
        
        # security feature
        uri = uri.replace("/..", '')

        # split hostname from resources
        resourceParts = uri.split('/', 1)
        hostname = resourceParts[0]
        print(f"hostname: {hostname}\n")
        resource = '/'
        if len(resourceParts) == 2:
            # Resource is the absolute uri with hostname and resource
            resource = resource + resourceParts[1]

        print (f"Requested resource:\t {resource}")

        cacheLocation = f"./{hostname}{resource}"
        if cacheLocation.endswith('/'):
            cacheLocation = cacheLocation + 'default'
        
        print(f"Cache location:\t\t{cacheLocation}")

        fileExists = os.path.isfile(cacheLocation)

        try:
            # Check whether the file exist in the cache
            cacheFile = open(cacheLocation, "r")
            outputdata = cacheFile.readlines()

            print ('Cache hit! Loading from cache file: ' + cacheLocation)
            # ProxyServer finds a cache hit
            # Send back contents of cached file
            # ~~~~ INSERT CODE ~~~~
            
            cacheResponse = ''
            for line in outputdata:
                cacheResponse += str(line) # bad memory use but it works

            clientSocket.sendall(cacheResponse)
            # ~~~~ END CODE INSERT ~~~~

            cacheFile.close()

        # Error handling for file not found in cache
        except IOError:
            if fileExists:
                #testing
                print('Error: File found but unreadable')

                clientResponse = ''
                # If we get here, the file exists but the proxy can't open or read it
                clientResponse = '500 Internal Server Error'

                # should then delete the file if its unusable

                print (f"Sending to the client:\n> {clientResponse}\n>")
                clientSocket.sendall(clientResponse + "\r\n\r\n")

            else:
                #testing
                print('\nFile not found in cache - connecting to origin server for file\n')
                
                originServerSocket = None
                # Create a socket to connect to origin server and store in originServerSocket
                originServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                print (f"Connecting to:\t\t {hostname}\n")
                try:
                    # Get the IP address for the connecting hostname
                    address = socket.gethostbyname(hostname)

                    print (address)

                    # Connect to the origin server
                    print('Creating originServerSocket' + '\n')
                    originServerSocket.connect( (address,80) )

                    print ('Connected to origin Server \n')

                    # Create a file object associated with this socket
                    # This lets us use file function calls
                    originServerFileObj = originServerSocket.makefile('wb', 0)

                    ogReqHeader = ''
                    ogReq = ''
                    
                    # Create origin server request line and headers to send
                    ogReq = f"{method} {resource} {version}"
                    ogReqHeader = f"Host: {hostname}"

                    # Construct the request to send to the origin server
                    request = ogReq + '\r\n' + ogReqHeader + '\r\n\r\n'

                    # Request the web resource from origin server
                    print ('Forwarding request to origin server:')
                    for line in request.split('\r\n'):
                        print (f'> {line}')

                    try:
                        print ('\r sending request to origin server')
                        originServerSocket.sendall(request.encode())
                        print('\r request sent successfully')
                    except socket.error:
                        sys.exit('Send failed')

                    print('\r writing origin server request to file')
                    originServerFileObj.write(request.encode())
                    print('\r request written to file')

                    # Get the response from the origin server
                    print ('\r response incoming')

                    #originServerSocket connected to server
                    response = originServerSocket.recv(BUFFER_SIZE)
                    print('\r response received: \n' + response.decode())

                    # --Send the response to the client--
                    #serversocket accepted connection from client
                    print('\r sending response to client')
                    clientSocket.sendall(response)
                    print ('\r response sent')

                    # finished sending to origin server - shutdown socket writes
                    originServerSocket.shutdown(socket.SHUT_WR)

                    print ('Request sent to origin server\n')

                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket
                    # and the corresponding file in the cache
                    cacheDir, file = os.path.split(cacheLocation)
                    print ('cached directory ' + cacheDir)
                    if not os.path.exists(cacheDir):
                        os.makedirs(cacheDir)
                    cacheFile = open(cacheLocation, 'wb')

                    # Save origin server response in the cache file
                    cacheFile.write(response)

                    print ('done sending')
                    originServerSocket.close()
                    cacheFile.close()
                    print ('cache file closed')
                    clientSocket.shutdown(socket.SHUT_WR)
                    print ('client socket shutdown for writing')
                except IOError as message:
                    sys.exit ('origin server request failed. ' + message)
        try:
            #testing
            print('closing socket')
            clientSocket.close()
        except:
            print ('Failed to close client socket')