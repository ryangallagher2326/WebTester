from socket import *
import ssl
import sys
from typing import List, Tuple
from text_parser import *
from socket_handler import *


def main():
    if (len(sys.argv)) != 2:
        print("Please enter one website")
        sys.exit(1)

    url = sys.argv[1]                                                                   #get first url
    url = url.strip()

    protocol, hostname, path = parse_url(url)                                           #extract the protocol, hostname, and path from url
    response, alpn_protocol = handle_socket(protocol, hostname, path)                   #get the server's response, and alpn_protocol
    header = get_header(response)                                                       #extract the header from the response
    status_code = get_status_code(header)                                               #get the status code from the header

    redirect_counter = 0

    while ((status_code == 301) or (status_code == 302)):                              #if it is a redirect, keep the same cycle going until we get to the final server
        print("Redirected\n")
        new_url = handle_redirect(header, protocol, hostname)                                         #This will be the new url we get from the redirect
        protocol, hostname, path, = parse_url(new_url)
        response, alpn_protocol = handle_socket(protocol, hostname, path)
        header = get_header(response)
        status_code = get_status_code(header)

        redirect_counter += 1
        if redirect_counter >= 5:
            break

    password_protected = False

    if ((status_code == 401) or (status_code == 403)):
        password_protected = True
    
    
    print(f"website: {url}")                                #print out the old url
    if (alpn_protocol == "h2"):
        print("1. Supports http2: yes")     
    else:
        print("1. Supports http2: no")

    
    cookie_list = get_cookies(header)                           #get the list of cookies
    print_cookies(cookie_list)                                  #print out the cookies

    if password_protected:
        print("3. Password-protected: yes")
    else:
        print("3. Password-protected: no")


def handle_redirect(header: str, protocol: str, hostname: str):                           #returns new url to go to
    lines = header.split("\r\n")

    for line in lines:
        line = line.strip()
        if line.lower().startswith("location"):
            location_list = line.split(":", 1)
            location = location_list[1].strip()

            if location.startswith("//"):
                return protocol + ":" + location
            if location.startswith("http://") or location.startswith("https://"):
                return location
            if location.startswith("/"):                     #if the redirect path is relative
                return protocol + "://" + hostname + location
            
            return protocol + "://" + hostname + "/" + location
            





if __name__ == "__main__":
    main()