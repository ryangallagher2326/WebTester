from socket import *
import ssl
import sys
from typing import List, Tuple


def parse_url(url: str) -> List[str]:            #Takes the url, and returns a list of the protocol, hostname, and path components
    url_list = []
    if url.startswith("http://"):
        protocol = "http"
        pro_len = len("http://")
        rest_of_url = url[pro_len:]             #gets rid of the part we already parsed
    elif url.startswith("https://"):
        protocol = "https"
        pro_len = len("https://")
        rest_of_url = url[pro_len:]
    else:                                       #there is no specified protocol
        protocol = "http"
        rest_of_url = url

    url_list.append(protocol)

    names = rest_of_url.split("/")
    hostname = names[0]
    url_list.append(hostname)                   #adds hostname to return list

    path = "/" + "/".join(names[1:]) if len(names) > 1 else "/" 

    url_list.append(path)

    return url_list

    
def get_cookies(header: str) -> List[List[str]]:                              #parses the cookies, returns a list of lists that each store information about each cookie
    cookie_list = []
    lines = header.split("\r\n")


    for line in lines:                                              #get the cookie lines
        expiry_value = False
        domain_value = False
        if line.lower().startswith("set-cookie:"):
            line_list = line.split(";")
            cookie = line_list[0]                                   #get just the cookie
            name_value = cookie.split(":", 1)      
            name = name_value[1]                                #gets the name of the cookie  
            name = name.strip()                       

            id_and_value = name.split("=", 1)                      #splits name and the value
            id = id_and_value[0]                                #gets the id of the cookie name
            
            for word in line_list:                                      #looking for expiry date and domain name
                word = word.strip()
                if word.lower().startswith("expires"):
                    expiry_list = word.split("=", 1)
                    date = expiry_list[1]
                    expiry_value = True

                elif word.lower().startswith("domain"):
                    domain_list = word.split("=", 1)
                    domain = domain_list[1]
                    domain_value = True
    
            if (expiry_value and domain_value):
                cookie_list.append([id, date, domain])

            elif (expiry_value and (not domain_value)):
                cookie_list.append([id, date, "0"])

            elif ((not expiry_value) and domain_value):
                cookie_list.append([id, "0", domain])

            else:
                cookie_list.append([id, "0", "0"])


    return cookie_list



def print_cookies(cookie_list):                                         #takes list of cookie information and prints results
    print("2. List of Cookies:")
    for element in cookie_list:
        name = element[0]
        date = element[1]
        domain = element[2]

        if (date == "0" and domain == "0"):                         #only name
            print(f"cookie name: {name}")                             #print out cookie name
        
        elif ((not date == "0") and domain == "0"):                 #only name and expiry date
            print(f"cookie name: {name}, expiry time: {date}")

        elif (date == "0" and (not domain == "0")):                      #only name and domain
            print(f"cookie name: {name}, domain name: {domain}")

        else:
            print(f"cookie name: {name}, expiry time: {date}; domain name: {domain}")
            

def get_header(response:str) -> str:                                        #gets just the header
    header_and_body = response.split("\r\n\r\n")
    header = header_and_body[0]
    return header


def get_status_code(header: str) -> int:                                    #gets the status code
    try:
        lines = header.split("\r\n")
        status_line = lines[0]
        status_line_list = status_line.split(" ")
        code = status_line_list[1]
        

        return int(code)
    except:
        print("Error: Please enter a valid URL with a valid path")
        sys.exit(1)