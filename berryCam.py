
#!/usr/bin/env python
#
#  BerryCam.py
#  BerryCam - Raspberry Pi Camera Controller for use with iOS devices
#
#  Created by James Moore on 17/08/2020
#  Copyright (c) 2013-2020 Fotosyn. All rights reserved.
#
#  Raspberry Pi is a trademark of the Raspberry Pi Foundation.
#  iOS is a trademark or registered trademark of Cisco in the U.S. and other countries and is used by Apple Inc. under license.
#


import http.server
import socketserver
import os
from urllib import parse

port = 8000
handler = http.server.SimpleHTTPRequestHandler

class BerryCamHandler (http.server.SimpleHTTPRequestHandler):
    
    print("B E R R Y C A M -- Listening on port ", port, flush=True)
    print("Please ensure your BerryCam App is installed and running on your iOS Device", flush=True)
    
    def do_GET(self):
        
        parsed_url = parse.urlsplit(self.path)
        parsed_query = parse.parse_qs(parsed_url.query)
        parsed_dictionary = dict(parse.parse_qsl(parsed_url.query))
        
        if parsed_url.path == "/berrycam":
            
            directory = 'berrycam/' + parsed_dictionary['ffolder']
            if not os.path.exists(directory):
                os.makedirs(directory)
              
            # Build up a raspistill command line string
            
            command = "raspistill -v" # Initiate command for Raspistill
            command += " -awb " +   parsed_dictionary['awb'] # Define WB
            command += " -mm " +   parsed_dictionary['mm'] # Define Metering Mode
            command += " -ev " + parsed_dictionary['ev'] # Define the Exposure Adjustment
            command += " -ex " +   parsed_dictionary['ex'] # Define Exposure Mode
            command += " -sh " + parsed_dictionary['sh'] # Define Image Sharpness
            command += " -br " + parsed_dictionary['br'] # Define Image Brightness
            command += " -co " + parsed_dictionary['co'] # Define Image Contrast
            command += " -sa " + parsed_dictionary['sa'] # Define Image Saturation
            command += " -ISO " + parsed_dictionary['iso'] # Define Image ISO
            command += " -drc " + parsed_dictionary['drc'] # Define Image dynamic range compres$

            if parsed_dictionary['ss'] != "1":
                command += " -ss " + parsed_dictionary['ss'] # Define shutter speed STILL TO BE IMPLEMENTED
                
            command += " -ifx " +   parsed_dictionary['ifx'] # Define Image Effect
            command += " -q " + parsed_dictionary['fquality'] # Define Image Quality
            command += " -w " + parsed_dictionary['fwidth'] # Define output image width
            command += " -h " + parsed_dictionary['fheight'] # Define output image height
            command += " -o berrycam/" + parsed_dictionary['ffolder'] + "/IMG-" + parsed_dictionary['fseq'] +".jpg"

            if parsed_dictionary['hf'] == "1":
              command += " -hf "
            else:
              command += ""

            if parsed_dictionary['vf'] == "1":
              command += " -vf "
            else:
              command += ""

            if 'gpsLat' in parsed_dictionary:
                command += " -gps"
                command += " -x GPS.GPSLatitude=" + parsed_dictionary['gpsLat']
                command += " -x GPS.GPSLongitude=" + parsed_dictionary['gpsLon']
                command += " -x GPS.GPSAltitude=" + parsed_dictionary['gpsAlt']
                command += " -x GPS.GPSLatitudeRef=" + parsed_dictionary['gpsLatRef']
                command += " -x GPS.GPSLongitudeRef=" + parsed_dictionary['gpsLonRef']
                command += " -x GPS.GPSImgDirection=1"
                command += " -x GPS.GPSTimeStamp=1"

            if parsed_dictionary['ao'] == "1":
              command += " -a 1024"
              command += " -a " + "\"" + parsed_dictionary['a'] + "\""
              command += " -ae " + parsed_dictionary['ae']

            os.system(command)
            self.send_response(200)
            self.end_headers()
            return
            
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)
            self.end_headers()
            return
        
        
with socketserver.TCPServer(("", port), BerryCamHandler) as httpd:
    httpd.serve_forever()