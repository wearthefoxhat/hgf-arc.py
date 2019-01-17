#!/usr/bin/env python
# Scipt Name: hgf-arc.py

# Author: Wearthefoxhat

# Version: 1.0
# Created: 17-Jan-19

# Description: This script reads the data received on localhost, port 10002 then acknowledges and puts it into arrays for further processing to the future developers taste.

import socket
import re
import time
import datetime

def HexToByte( hexStr ):

    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

    return ''.join( bytes )

def process_SIA(hexF,ascF,hexN,ascN,hexA,ascA,IP):

    #Function to be developed to extract info desired and process into other data stores i.e MQTT / SQL / LogFile etc.

    #IP will contain panel IP address
    #ascF will contain account number
    #ascN will contain N data
    #ascA will contain A data

    #the first hex byte is usually the offset length of the packet discounting the first 2 bytes and last byte.

    #this point is where you could implement IP addr checking against account number for security where the data is silently not processed any further.

    #the world is now your oyster to manipulate the data and process.


    return True


def process_msg(hex_arr, asc_arr, addr):

    #hex_arr should look something like....
    # [[x,x,x,etc],[x,x,x,etc],[x,x,x,etc],[x,x,x,etc]]
    #asc_arr
    # [[A,B,C,etc],[A,B,C,etc],[A,B,C,etc],[A,B,C,etc]]

    for i in range (0,len(hex_arr)):
       print hex_arr[i]
       print asc_arr[i]
       print "##################################"

    #First packet is usually Account Number
    #Second packet is the N Data block
    #Third packet is the A Data block

    #Sometimes the PANEL will send multiple job lots of (3 packet) messages.  So we need to account for this.

    #Final Packet is signoff usually with 3 hex bytes.

    #Usual handling one message report per session.
    if len(hex_arr) == 4:
       process_SIA(hex_arr[0],asc_arr[0],hex_arr[1],asc_arr[1],hex_arr[2],asc_arr[2], addr[0])

    #Example to handle 2 lots of messages in the same session.  Occours infrequently but needs to be handled.
    if len(hex_arr) == 7:
       process_SIA(hex_arr[0],asc_arr[0],hex_arr[1],asc_arr[1],hex_arr[2],asc_arr[2], addr[0])
       process_SIA(hex_arr[3],asc_arr[3],hex_arr[4],asc_arr[4],hex_arr[5],asc_arr[5], addr[0])

    # for three messages it would be len=10 and four is len=13 etc etc.



def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'
    port = 10002
    s.bind((host, port))  #Binding the port with host
    global var2

    while True:

        try:

            s.listen(5)
            c, addr = s.accept() #Establishing connection with the client.
            print 'Got connection from', addr

            #Setup Arrays for multiple packets as they arrive in the session from PANEL
            HEXarr = []
            ASCIIarr = []

            while True:
                data = c.recv(1024)
                if not data:
                    break
                #this is the ACK response string sent to the panel.  which then tells PANEL to send next packet
                #otherwise the panel will keep sending packet one.  This only works with unencrypted transmission.
                c.send('\x00\x38\xff')

                #Setup Arrays for individual bytes as they arrive in packet the session from PANEL
                HEXmsg = []
                ASCIImsg = []
                #Go through each packet and dump each byte into HEX array.
                #At same time convert each HEX byte into ASCII and put into matching array.
                #Reason is printing the string of recv data does not format that well due to non ascii chars.  
                #So Char Array is needed further along to get the data out and format it systematically into outputs like MQTT & SQL.
                for i in range (0,len(data)):
                   HEXmsg.append(hex(ord(data[i])))
                   ASCIImsg.append(chr(int(HEXmsg[i],16)))
                HEXarr.append(HEXmsg)
                ASCIIarr.append(ASCIImsg)
            c.close()

            #Call function to process the arrays recieved from the session with the Panel
            process_msg(HEXarr,ASCIIarr, addr)

        except socket.error:
            break

if __name__ == '__main__':
    main()
