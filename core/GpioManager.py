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
#      Purpose:
#
#
#      Clone at: https://github.com/rogermanich/gn-pi.git
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Rpi.GPIO not installed")

from time import sleep as sleep


class GpioManager:
    """
        Class to handle GPIO pins on Rasberry based on RPi.GPIO library.
    """

    def __init__(self):
        """

        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.channels = []
        self.gpioIds = []
        # configure it according your needs
        self.ON = GPIO.LOW
        self.OFF = GPIO.HIGH

    def getchannel(self, channelid: str) -> int:
        """
        :param channelid: logic name of channel e.g. PIPE-1
        :return: index of channel in the list or -1 if it doesn't exist
        :rtype: integer
        """
        try:
            index = self.channels.index(channelid)
            return index
        except ValueError:
            return -1

    def addoutputchannel(self, channelid: str, gpioid: int):
        """
        :purpose: Configure GPIO pin as OUTPUT and define mapping for GPIO pin.
                  We can reconfigure GPIO pins but keep same channel names.
        :param channelid: Logic name of GPIO pin e.g. PIPE-1
        :param gpioid: BCM codification of GPIO pin
        :return: None
        :rtype: None
        """
        if self.getchannel(channelid) < 0:
            self.channels.append(channelid)
            self.gpioIds.append(gpioid)
            GPIO.setup(gpioid, GPIO.OUT,pull_up_down=GPIO.PUD_OFF,initial=1)

    def switchoff(self, channel: str) -> bool:
        """ On SSR GPIO.HIGH open the channel => Power Off
        :param channel: Logic name of GPIO pin e.g. PIPE-1
        :return: true if succeed, false if channel is not defined.
        """
        index = self.getchannel(channel)
        if index >= 0:
            GPIO.output(self.gpioIds[index], self.OFF)
            return True
        else:
            return False

    def switchonbulk(self, channellist, ptime=0):
        """

        :param channellist: list of Logic name of GPIO pin e.g ["PIPE-1","PIPE-2"]
        :param ptime: time to keep channels on. 0 means always.
        :return: None
        """
        for channel in channellist:
            self.switchon(channel)
        if ptime > 0:
            sleep(ptime)
            for channel in channellist:
                self.switchoff(channel)

    def switchon(self, channel, ptime=0):
        """ On SSR GPIO.Low close the channel => Power On
        :param channel:
        :param ptime:
        :return:
        """
        index = self.getchannel(channel)
        if index >= 0:
            GPIO.output(self.gpioIds[index], self.ON)
            if ptime > 0:
                sleep(ptime)                
                self.switchoff(self.gpioIds[index])
            return True
        else:
            return False

    def state(self):
        """ On SSR status true means Power On
        :return: list of GPIO states
        """
        states = []
        for channel in self.channels:
            index = self.getchannel(channel)
            if index >= 0:
                if GPIO.input(self.gpioIds[index]) == self.ON:
                    states.append(True)
                else:
                    states.append(False)
        else:
            # Channel not defined
            states.append(-1)
        return states

    def shutdown(self):
        """

        """
        # switch off all configured ports
        # clean
        try:
            for channel in self.gpioIds:
                self.switchoff(channel)
            GPIO.cleanup()
        except (RuntimeError, RuntimeWarning):
            print("Error while shutting down!")

if __name__ == "__main__":
    a = GpioManager()
    a.addoutputchannel("Pipe-1", 4)
    a.addoutputchannel("Pipe-2", 17)
    a.addoutputchannel("Main Terrace Lights", 27)
    a.addoutputchannel("Secondary Terrace Lights", 22)
    a.switchon("Pipe-1", 3)
    a.switchonbulk(["Pipe-1", "Pipe-2", "Main Terrace Lights"], 3)
    a.switchon("Pipe-1")
    print(a.state())
    a.shutdown()
