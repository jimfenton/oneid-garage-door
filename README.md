## About

oneid-garage-door is a simple application for controlling a garage
door opener using a OneID identity. A short demo can be seen on
[YouTube](https://www.youtube.com/watch?v=1dw12DsCMGU).

The application consists of three Python applications intended to run
as CGI applications from a web server such as Apache:

* OneIDgarage.py - Displays a page at which the user signs in with OneID in
order to operate (close or open) the garage door. Reads and displays
the current state of the door from the Raspberry.

* OneIDvalidate.py - Validates the user's sign in using the OneID Helper
Service.

* OneIDoperate.py - Determines if the authenticated user is authorized to
open the door, and if so, directs the Raspberry Pi to activate a
relay to do so.  Logs the action in syslog.

It also includes:

* GarageIcon.png, a garage door icon that is referenced by garage.py
if bookmarking the sign in page on an iPhone.

* GarageOpen.png and GarageClosed.png, images used to show the open and closed
state of the door on the opening screen.

* garageinterface.pdf and garageinterface.graffle, a schematic diagram for the interface hardware.

* hardware.md, a description of the interface hardware

### Caution

This program potentially gives you the ability to open and close a
garage door from basically anywhere.  This represents a small but
non-zero risk to safety and personal property. For this reason, I
recommend connecting the Raspberry Pi to the network behind a
firewall, so that it is only accessible from the local network where
the user is more likely to be in proximity to the door when operating
it.

### Python Requirements

This application uses the:

* [Raspberry Pi GPIO
  daemon](https://github.com/jimfenton/raspberry-gpio-daemon), used to
  communicate with the GPIO port from the web server application.

* [OneID Python SDK](http://github.com/OneID/oneid-python-sdk). As of
  this writing, this SDK was not working properly with standard
  Raspbian Linux, due to issues with the SSL version used by the
  Requests library it references. If it hangs in the verify service
  (when referencing https://keychain.oneid.com), you might want
  instead to use [my
  fork](https://github.com/jimfenton/oneid-python-sdk).

## Installation

Install the Python programs in an executables directory in the web
server.  This might be under cgi-bin (with other web pages redirecting
there) or by enabling execution directly from the directory referenced
by the user.  This is probably not a good security practice in
general, but since a given Raspberry Pi processor is likely not to be
used for other things, might be reasonable here.

If you use SSL in conjunction with OneID authentication, which is
always recommended, you will need to obtain and install X.509
certificates for the server.

Write access to the directory containing the authorized user list,
OneIDgarage.cfg, is needed to add new authorized garage door operators.

## Operation and Administration

The garage door opener application maintains a list of authorized
garage door operators in the file OneIDgarage.cfg, which is a pickle
archive. It initially has an empty list of authorized users.  To
authorize a user, press and hold the Learn button (see schematic)
while that user signs in and the user will be authorized for future
use of the door.  There is currently no mechanism to deauthorize a
user; you probably need to clear garage.cfg and reauthorize all users
or write a simple program to remove the one user from the database.

If you want to see who is operating the door when, operate.py logs
garage door actions to syslog. Note that the name shown in syslog is a
OneID attribute provided with authentication, and is self-asserted by
the user. It should not be relied upon to be authoritative.

## Future work

Some ideas for enhancements:

* Establish a tier of administrative users who could authorize users
  who have tried and failed to open the garage door and de-authorize
  users when needed. This is probably not needed for the typical
  garage door, but might be useful in office situations, for example.

* Set dates and times for access to certain users. For example, you
  might want to authorize access by the gardener on Tuesdays between 8
  am and 5 pm, but not at other times.

## Change Log

### 0.1.0

* Initial version.

### 0.1.1

* Added open and closed icons to show door state more easily
* Corrected script locations to use cgi-bin/ in pathnames
* Added OneID to names of files in cgi-bin/ to distinguish them from non-OneID versions that may also be present in that directory
