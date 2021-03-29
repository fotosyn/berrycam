
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
from time import sleep
import picamera
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

            print("Capture")
            directory = 'berrycam/' + parsed_dictionary['ffolder']
            if not os.path.exists(directory):
                os.makedirs(directory)

            #Build up a PiCamera command line string
            with picamera.PiCamera() as camera:

                # Fix for differences in AWB call for sunlight setting
                if parsed_dictionary['awb'] == "sun":
                    parsed_dictionary['awb'] = "sunlight"

                # Fix for differences in AWB call for cloudy setting
                if parsed_dictionary['awb'] == "cloud":
                    parsed_dictionary['awb'] = "cloudy"

                # Fix for differences in AWB call for greyworld setting - incompatible with PiCamera
                if parsed_dictionary['awb'] == "greyworld":
                    parsed_dictionary['awb'] = "auto"

                camera.awb_mode = parsed_dictionary['awb']
                camera.brightness = int(parsed_dictionary['br'])
                camera.contrast = int(parsed_dictionary['co'])
                camera.drc_strength = parsed_dictionary['drc']
                camera.exposure_compensation = int(parsed_dictionary['ev'])
                camera.exposure_mode = parsed_dictionary['ex']

                # Watercolour renamed to Watercolor in PiCamera
                if parsed_dictionary['ifx'] == "watercolour":
                    parsed_dictionary['ifx'] = "watercolor"

                # Whiteboard not available with PiCamera
                if parsed_dictionary['ifx'] == "whiteboard":
                    parsed_dictionary['ifx'] = "none"

                camera.image_effect = parsed_dictionary['ifx']
                camera.iso = int(parsed_dictionary['iso'])
                camera.meter_mode = parsed_dictionary['mm']
                camera.saturation = int(parsed_dictionary['sa'])
                camera.sharpness = int(parsed_dictionary['sh'])

                if parsed_dictionary['vf'] == "1":
                    camera.vflip = True
                
                if parsed_dictionary['hf'] == "1":
                    camera.hflip = True

                # GPS coordinates from device to add to EXIF data 
                if 'gpsLat' in parsed_dictionary:
                    camera.exif_tags['GPS.GPSLatitude'] = "%s/1,%s/1,%s/100" % (parsed_dictionary['gpsLatD'],parsed_dictionary['gpsLatM'],parsed_dictionary['gpsLatS'])
                    camera.exif_tags['GPS.GPSLongitude'] = "%s/1,%s/1,%s/100" % (parsed_dictionary['gpsLonD'],parsed_dictionary['gpsLonM'],parsed_dictionary['gpsLonS'])
                    camera.exif_tags['GPS.GPSAltitude'] = parsed_dictionary['gpsAlt']
                    camera.exif_tags['GPS.GPSAltitudeRef'] = "0" if parsed_dictionary['gpsAlt'] != "0" else "1"
                    camera.exif_tags['GPS.GPSLatitudeRef'] = parsed_dictionary['gpsLatRef']
                    camera.exif_tags['GPS.GPSLongitudeRef'] = parsed_dictionary['gpsLonRef']
                    camera.exif_tags['GPS.GPSImgDirection'] = "1"
                    camera.exif_tags['GPS.GPSTimeStamp'] = "1"

                # Annotations for captured image
                if parsed_dictionary['ao'] == "1":
                    camera.annotate_foreground = picamera.Color("#%s" % parsed_dictionary['affg'])
                    camera.annotate_background = picamera.Color("#%s" % parsed_dictionary['afbg'])
                    camera.annotate_text = " %s " % parsed_dictionary['a']
                    camera.annotate_text_size = int(parsed_dictionary['afs'])

                output_file = "berrycam/" + parsed_dictionary['ffolder'] + "/IMG-" + parsed_dictionary['fseq'] +".jpg"
                camera.start_preview()
                camera.resolution = (int(parsed_dictionary['fwidth']), int(parsed_dictionary['fheight']))
                sleep(2)
                camera.capture(output_file, format="jpeg", quality=int(parsed_dictionary['fquality']))

            self.send_response(200)
            self.end_headers()
            return

        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)
            self.end_headers()
            return


with socketserver.TCPServer(("", port), BerryCamHandler) as httpd:
    httpd.serve_forever()
