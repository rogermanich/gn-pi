#!/usr/bin/python3
# /etc/init.d/GNShutdownGPIO.py
### BEGIN INIT INFO
# Provides:          GNShutdownGPIO.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

# Copyright (c) 2015-2018 "Roger Manich"
#
#      this file and included software is not free software: you can
#      redistribute it and/or modify it under the terms of the GNU General
#      Public License as published by the Free Software Foundation, either
#      version 3 of the License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.#
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#      Contributors:
#        Roger Manich roger.manich@gmail.com
#        Creation date: 2018-07-26
#
#      Purpose: Shutdown all Configured GPIO gates in order to 
#               start in known state.
#
#      Clone at: https://github.com/rogermanich/gn-pi.git
import core.GpioManager as GpioManager

print("(c) 2018 Garden Nursery v1.0.0")
print("")
print("Starting to clean GPIO Ports")
Manager = GpioManager.GpioManager()
Gates = [["Pipe-1",4],["Pipe-2",17],["Pipe-3",27],["Pipe-4",22]]
for gate in Gates:
        print("Configuring gate " + str(gate[0]) + " as OUTPUT.")
        Manager.addoutputchannel(gate[0],gate[1])        
print("Clean GPIO Ports... Started")
Manager.shutdown()
print("GPIO Ports Cleaned.")
