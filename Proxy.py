# Include the libraries for socket and system calls
import socket
import sys
import os
import argparse
import re

# 1MB buffer size
BUFFER_SIZE = 1000000

parser = argparse.ArgumentParser()
parser.add_argument('hostname', help='the IP Address Of Proxy Server')
parser.add_argument('port', help='the port number of the proxy server')
args = parser.parse_args()

# Create a server socket, bind it to a port and start listening
# The server IP is in args.hostname and the port is in args.port
# bind() accepts an integer only
# You can use int(string) to convert a string to an integer
# ~~~~ INSERT CODE ~~~~

host = args.hostname
port = int(args.port)

# ~~~~ END CODE INSERT ~~~~

try:
  # Create a server socket
  # ~~~~ INSERT CODE ~~~~
  serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # ~~~~ END CODE INSERT ~~~~
  print ('Connected socket')
except:
  print ('Failed to create socket')
  sys.exit()

try:
  # Bind the the server socket to a host and port
  # ~~~~ INSERT CODE ~~~~
  serversocket.bind(( host, port ))
  # ~~~~ END CODE INSERT ~~~~
  print ('Port is bound')
except:
  print('Port is in use')
  sys.exit()

try:
  # Listen on the server socket
  # ~~~~ INSERT CODE ~~~~
  serversocket.listen(5)
  # ~~~~ END CODE INSERT ~~~~
  print ('Listening to socket')
except:
  print ('Failed to listen')
  sys.exit()

#not entirely sure while what is true...
while True:
  print ('Waiting connection...')

  clientSocket = None
  try:
    # Accept connection from client and store in the clientSocket
    # ~~~~ INSERT CODE ~~~~
    (clientSocket,address) = serversocket.accept()
    # ~~~~ END CODE INSERT ~~~~
    print ('Received a connection from: ' + args.hostname)
  except:
    print ('Failed to accept connection')
    sys.exit()

  message = 'METHOD URI VERSION'
  # Get request from client
  # and store it in message
  # ~~~~ INSERT CODE ~~~~
  message = clientSocket.recv(BUFFER_SIZE)
  # ~~~~ END CODE INSERT ~~~~

  print ('Received request:')
  print ('< ' + message.decode('utf-8'))

  # Extract the parts of the HTTP request line from the given message
  requestParts = message.split()
  method = requestParts[0]
  URI = requestParts[1]
  version = requestParts[2]

  print ('Method:\t\t' + method.decode('utf-8'))
  print ('URI:\t\t' + URI.decode('utf-8'))
  print ('Version:\t' + version.decode('utf-8'))
  print ('')

  # Remove http protocol from the URI
  URI = re.sub('^(/?)http(s?)://', '', URI, 1)

  # Remove parent directory changes - security
  URI = URI.replace('/..', '')

  # Split hostname from resource
  resourceParts = URI.split('/', 1)

  hostname = resourceParts[0]
  print ('hostname: ' + hostname + '\n') #testing
  resource = '/'

  if len(resourceParts) == 2:
    # Resource is absolute URI with hostname and resource
    resource = resource + resourceParts[1]

  print ('Requested Resource:\t' + resource)

  cacheLocation = './' + hostname + resource #eg ./autoidlab.cs.adelaide.edu.au/default
  if cacheLocation.endswith('/'):
    cacheLocation = cacheLocation + 'default'

  print ('Cache location:\t\t' + cacheLocation)

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
      # What would be the appropriate status code and message to send to client?
      # store the value in clientResponse
      # ~~~~ INSERT CODE ~~~~
      clientResponse = '500 Internal Server Error'

      # ~~~~ END CODE INSERT ~~~~

      print ('Sending to the client:')
      print ('> ' + clientResponse)
      print ('>')
      clientSocket.sendall(clientResponse + "\r\n\r\n")

    else:
      #testing
      print('\n' + 'File not found in cache - connecting to origin server for file' + '\n')
      
      originServerSocket = None
      # Create a socket to connect to origin server
      # and store in originServerSocket
      # ~~~~ INSERT CODE ~~~~
      originServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      # ~~~~ END CODE INSERT ~~~~

      print ('Connecting to:\t\t' + hostname + '\n')
      try:
        # Get the IP address for a hostname
        address = socket.gethostbyname(hostname)

        print (address)

        # Connect to the origin server
        # ~~~~ INSERT CODE ~~~~
        print('Creating originServerSocket' + '\n')
        originServerSocket.connect( (address,80) )
        # ~~~~ END CODE INSERT ~~~~

        print ('Connected to origin Server \n')

        # Create a file object associated with this socket
        # This lets us use file function calls
        originServerFileObj = originServerSocket.makefile('+', 0)

        originServerRequestHeader = ''
        originServerRequest = ''
        # Create origin server request line and headers to send
        # and store in originServerRequestHeader and originServerRequest
        # originServerRequest is the first line in the request and
        # originServerRequestHeader is the second line in the request
        # ~~~~ INSERT CODE ~~~~

        originServerRequest = method + ' ' + resource + ' ' + version
        originServerRequestHeader = 'Host: ' + hostname

        # ~~~~ END CODE INSERT ~~~~

        # Construct the request to send to the origin server
        request = originServerRequest + '\r\n' + originServerRequestHeader + '\r\n\r\n'

        # Request the web resource from origin server
        print ('Forwarding request to origin server:')
        for line in request.split('\r\n'):
          print ('> ' + line)

        try:
          print ('\r sending request to origin server')
          originServerSocket.sendall(request)
          print('\r request sent successfully')
        except socket.error:
          print ('Send failed')
          sys.exit()

        print('\r writing origin server request to file')
        originServerFileObj.write(request)
        print('\r request written to file')

        # Get the response from the origin server
        # ~~~~ INSERT CODE ~~~~
        print ('\r response incoming')
        #originServerSocket connected to server
        response = originServerSocket.recv(BUFFER_SIZE)
        print('\r response received: \n' + response)
        # ~~~~ END CODE INSERT ~~~~

        # Send the response to the client
        # ~~~~ INSERT CODE ~~~~
        #serversocket accepted connection from client
        print('\r sending response to client')
        clientSocket.sendall(response)
        print ('\r response sent')
        # ~~~~ END CODE INSERT ~~~~

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
        # ~~~~ INSERT CODE ~~~~
        cacheFile.write(response)
        # ~~~~ END CODE INSERT ~~~~

        print ('done sending')
        originServerSocket.close()
        cacheFile.close()
        print ('cache file closed')
        clientSocket.shutdown(socket.SHUT_WR)
        print ('client socket shutdown for writing')
      except IOError as message:
        print ('origin server request failed. ' + message)
  try:
    #testing
    print('closing socket')
    clientSocket.close()
  except:
    print ('Failed to close client socket')
