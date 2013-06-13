# Garage interface hardware

The interface in the accompanying schematic was designed to work with
a Chamberlain Lift-Master Model 1265 Garage Door Opener. The relay
interface to operate the garade door opener switch should work with
virtually any garage door opener, but the sense circuitry to determine
if the garage door is up or down is considerably more specialized.

## External connections

The garage door opener interface has three external connections:

### J1

J1 is a 26-pin ribbon cable to the Raspberry Pi GPIO
connector. Connections are straight-through, pin-to-pin.

### TB1

Wires from the two terminals of TB1 should be connected across (in
parallel with) the manual push-button used to operate the door. The
Model 1265 actually uses this connection for multiple purposes, such
as a control to turn the garage light on and off, but the interface
does not interfere with these functions.

### TB2

Two wires and ground connection from TB2 allow the interface to sense
the state of the garage door limit switches within the garage door
opener mechanism. Connecting these requires that one take the cover
off the mechanism and connect (probably solder) to the wires coming
from switch contacts.  Be sure and unplug the garage door opener while
doing do, high voltages are present and a mechanical hazard exists if
the motor starts running.

## Circuit Description

The driver circuit consists of a ULN2803A Darlington driver driving a
normally-open, diode-clamped relay. Be sure to observe the proper
polarity of the relay diode or it will effectively short out power to
the relay. An optional LED and current-limiting diode are also shown
to make it easier to observe the operation of the interface.

The Learn switch is simply a normally-open pushbutton on the GPIO 18
pin. Software-programmable pull-up is used so no external pull-up
resistor is required.

The sense circuit consists of two more sections of the ULN2803A
driver. These are connected to the TB2 connections through 10K ohm
resistors to provide a high-impedance connection to the garage door
circuit so as not to disturb its position sensing circuitry. The GPIO
connections again use software-programmable pull-up so no external
pull-up is required.

## Part sources

I was able to find virtually all of the parts I needed at
[Jameco](http://www.jameco.com) in Belmont, California but they should
be available from a wide range of sources.

