#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
import sys
import time
import RPi.GPIO as GPIO

PORT_NUMBER = 8080

mode=GPIO.getmode()

GPIO.cleanup()

l_Forward=12
l_Backward=16
r_Forward=18
r_Backward=22
sleeptime=1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(l_Forward, GPIO.OUT)
GPIO.setup(l_Backward, GPIO.OUT)
GPIO.setup(r_Forward, GPIO.OUT)
GPIO.setup(r_Backward, GPIO.OUT)

def forward():
    GPIO.output(l_Forward, GPIO.HIGH)
    GPIO.output(l_Backward, GPIO.LOW)
    GPIO.output(r_Forward, GPIO.HIGH)
    GPIO.output(r_Backward, GPIO.LOW)

def reverse():
    GPIO.output(l_Forward, GPIO.LOW)
    GPIO.output(l_Backward, GPIO.HIGH)
    GPIO.output(r_Forward, GPIO.LOW)
    GPIO.output(r_Backward, GPIO.HIGH)

def left():
    GPIO.output(l_Forward, GPIO.LOW)
    GPIO.output(l_Backward, GPIO.HIGH)
    GPIO.output(r_Forward, GPIO.HIGH)
    GPIO.output(r_Backward, GPIO.LOW)

def right():
    GPIO.output(l_Forward, GPIO.HIGH)
    GPIO.output(l_Backward, GPIO.LOW)
    GPIO.output(r_Forward, GPIO.LOW)
    GPIO.output(r_Backward, GPIO.HIGH)

def stop():
    GPIO.output(l_Forward, GPIO.LOW)
    GPIO.output(l_Backward, GPIO.LOW)
    GPIO.output(r_Forward, GPIO.LOW)
    GPIO.output(r_Backward, GPIO.LOW)

#This class will handles any incoming request from
#the controller 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            # Send the html message
            if self.path == "/connect":
                print('Client Connected')
                self.wfile.write(bytes('{"s": "p"}', "utf-8"))
            if self.path == "/left":
                print('{0} says Turn Left'.format(self.client_address))
                left()
                self.wfile.write(bytes('{"s": "p"}', "utf-8"))
            if self.path == "/right":
                print('{0} says Turn right'.format(self.client_address))
                right()
                self.wfile.write(bytes('{"s": "p"}', "utf-8"))
            if self.path == "/forward":
                print('{0} says Go Forward'.format(self.client_address))
                forward()
                self.wfile.write(bytes('{"s": "p"}', "utf-8"))
            if self.path == "/reverse":
                print('{0} says Go back'.format(self.client_address))
                reverse()
                self.wfile.write(bytes('{"s": "p"}', "utf-8"))
            if self.path == "/stop":
                print('{0} says stopped'.format(self.client_address))
                stop()
                self.wfile.write(bytes('{"s": "p"}', "utf-8"))
            return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming http requests
	server.serve_forever()

except KeyboardInterrupt:
    GPIO.cleanup()
    print('^C received, shutting down the web server')
    server.socket.close()