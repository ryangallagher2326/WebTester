from socket import *
import ssl
import sys
from typing import List, Tuple


def handle_socket(protocol: str, hostname: str, path: str):             #handles the socket behavior, connecting, http request and response, and returns the response and the http type
    try:
        if protocol == "http":                                                #determine port and if we can use alpn to find out if the server can support h2
            port = 80
            soc = socket(AF_INET, SOCK_STREAM)                              #create our socket
            remote_socket = (hostname, port)
        elif protocol == "https":
            soc2 = socket(AF_INET, SOCK_STREAM)                             #create a socket just to see if the server supports h2
            context = ssl.create_default_context()                          #create the TLS context so we can perform the alpn
            context.set_alpn_protocols(["h2", "http/1.1"])
            soc2 = context.wrap_socket(soc2, server_hostname=hostname)        #wrap the socket with the TLS context
            port = 443
            remote_socket = (hostname, port) 
            soc2.connect(remote_socket)                                     #connect to the remote socket
            http_version = soc2.selected_alpn_protocol()                    #get http_version
            soc2.close()                                                    #close temproary socket

            soc = socket(AF_INET, SOCK_STREAM)                              #open main socket

            context = ssl.create_default_context()                          #create TLS context for our main connection 
            context.set_alpn_protocols(["http/1.1"])                          #we can only use http/1.1
            soc = context.wrap_socket(soc, server_hostname=hostname)        #wrap our main socket in TLS
            remote_socket = (hostname, port)

                    
        soc.connect(remote_socket)                                           #connect to desired remote socket

        
        request = (f"GET {path} HTTP/1.1\r\n"
                f"Host: {hostname}\r\n"
                "Connection: close\r\n"
                    "\r\n"
                )
    
        request_encoded = request.encode("utf-8")               #turn our request string into bytes to get it ready to send


        soc.sendall(request_encoded)

        response = b""
        words = soc.recv(3000)
        response += words
        while words:
            words = soc.recv(3000)
            response += words

        response_decoded = response.decode("utf-8", errors="replace")

        print(response_decoded)


        if protocol == "https":                             #return the http_version we found through the TLS handshake with ALPN
            soc.close()
            return response_decoded, http_version
        else:
            soc.close()
            return response_decoded, "not_yet_decided"


    except gaierror:
        print("Error: Please enter a valid URL")
        sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)