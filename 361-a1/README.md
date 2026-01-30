# WebTester

## Description
WebTester is a Python program that sends an HTTP/HTTPS request to a valid server, receives a response, and prints out the following information regarding the server, if it supports HTTP/2, all of the cookies the server sends back, and if the page is password protected. Before this, this version of WebTester also prints out the word "redirect" when the request has been redirected (301/02).

## How to run
'''bash
python3 WebTester.py <url>