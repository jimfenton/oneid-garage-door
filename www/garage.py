#!/usr/bin/python

# garage.py - Prompt page for garage door opener application
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

from oneid import OneID
import socket

# Send a command to the GPIO daemon and return the result
def gpio(cmd):
   s.send(cmd+'\n')
   return s.recv(64)[0:-1]

authn = OneID()

# Open socket to communicate with gpiod, and determine door state

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sockfile = "/var/run/gpiod.sock"

s.connect(sockfile)

doorclosed = gpio("input 24")
dooropen = gpio("input 26")

s.close()

# Interpret door state

if doorclosed == "true":
   if dooropen == "true":
      state = "invalid"
      action = "operate"
   else:
      state = "closed"
      action = "open"
else:
   if dooropen == "true":
      state = "open"
      action = "close"
   else:
      state = "undetermined"
      action = "operate"

# Render web page

print """Content-Type: text/html

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
  <title>Garage Door Opener</title>
  <meta name="viewport" content="width=device-width"/>
  <link rel="apple-touch-icon" href="/GarageIcon.png"/>
</head>
<body>
<div align="center">
"""

if state == "closed":
   print '<img src="/GarageClosed.png"/>'
else:
   print '<img src="/GarageOpen.png"/>'

print authn.script_header

print "<h1>Garage door is "+ state + "</h1>"

print "<h2>Sign in with OneID to "+action+":</h2>"

print authn.draw_signin_button("http://garage.bluepopcorn.net/cgi-bin/validate.py?state="+state,"personal_info[first_name] personal_info[last_name]")

print "</div></body></html>"
