#!/usr/bin/python

# operate.py - Check authorization and operate the garage door
#
# Copyright (c) 2013 Jim Fenton
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import cgi
from oneid import OneID

import sys
import os
import socket
import time
import syslog
import pickle

# Debugging
import cgitb
cgitb.enable()

# Send a command to the GPIO daemon and return the result
def gpio(cmd):
   s.send(cmd+'\n')
   return s.recv(64)[0:-1]

print """Content-Type: text/html

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
  <title>Garage Door</title>
  <meta name="viewport" content="width=device-width"/>
</head>
<body>
<div align="center">
"""


form = cgi.FieldStorage()
if "sessionid" not in form:
   print "<H1>Error</H1>"
   print "Authentication failure - sessionid not found"
   print "</body></html>"
   exit()

try:
   with open("garage.cfg","r") as f:
      users = pickle.load(f)
      f.close()

except IOError:
   users = []

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sockfile = "/var/run/gpiod.sock"

s.connect(sockfile)

authn = OneID()
sess = authn.get_session(form["sessionid"].value)

descrip = sess["uid"]+" ("+sess["attr"]["personal_info"]["first_name"]+" "+sess["attr"]["personal_info"]["last_name"]+")"

mode = gpio("input 12")
if mode == "true":  #Normal mode, LEARN not pressed

   if sess["uid"] in users:
      try:
         if gpio("output 11 high") != "ok":
            raise RuntimeError
         if gpio("output 16 high") != "ok":
            raise RuntimeError
         time.sleep(0.5)
         if gpio("output 11 low") != "ok":
            raise RuntimeError
         if gpio("output 16 low") != "ok":
            raise RuntimeError
         syslog.syslog("Door operated for user "+descrip)
         print "<h2>Door operating</h2>"
      except RuntimeError:
         print "<h2>Error response from gpiod</h2>"
   else:
      print "<h2>User not authorized</h2>"
      syslog.syslog("Unauthorized user "+descrip)

elif mode == "false":  # LEARN mode

   if sess["uid"] in users:
      print "<h2>User already authorized</h2>"
      syslog.syslog("User already authorized: "+descrip)
   else:
      users.append(sess["uid"])
      try:
         with open("garage.cfg","w") as f:
            pickle.dump(users, f)
            f.close()
            print "<h2>User authorization added</h2>"
            syslog.syslog("User authorization added: "+descrip)
      except IOError:
         print "<h2>Error: Unable to add user authorization</h2>"
         syslog.syslog("Error adding user authorization: "+descrip)

else:
   print "<h2>Error: Unable to read LEARN button</h2>"

print "</div></body></html>"
