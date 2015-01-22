""" Module contains classes/function for work with DISKPART utility
"""
from subprocess import Popen, PIPE
import re
import ctypes
import locale

from DiskUtilityModule import DiskUtilExceptions, DiskUtilityInterface
import WinLocaleSettings
from SubprocessInteractive import InteractiveCommand


class WindowsDiskUtility(DiskUtilityInterface):
    def __init__(self, defaultEncoding='866'):
        """ Class wrapper for DISPART utility
        :param defaultEncoding: (str) Windows console output encoding
        :return: WindowsDiskUtility object
        """
        self.defaultEcoding = defaultEncoding
        #determin locale language
        windll = ctypes.windll.kernel32
        language = locale.windows_locale[ windll.GetUserDefaultUILanguage() ]
        self._locale = self._getLocale(language)
        #init Popen connection to diskpart
        try:
            p = Popen(["diskpart"], stdin=PIPE, stdout=PIPE )
            prompt = re.compile(r"^DISKPART>", re.M)
            self.cmd = InteractiveCommand(p, prompt)
        except WindowsError, e:
            raise DiskUtilExceptions('Cannot start DISKPART utility! Err: ' + str(e.winerror))

    def __del__(self):
        """ Close DISKPART connection
        :return:
        """
        self.cmd.command("exit")

    def _getLocale(self, lang='en'):
        """ factory method for LocaleInterface
        :param lang: (str) language abbr
        :return: (LocaleInterface object) corresponding current language
        """
        if 'en' in lang:
            return WinLocaleSettings.EnLocale()
        elif 'ru' in lang:
            return WinLocaleSettings.RuLocale()

    def _execDiskpartCmd(self, command):
        """ Execute DISKPART command
        :param command: (str) Command to execute
        :return: DISKPART output
        Raises:
          DiskpartException: If command is not valid
        """
        out = self.cmd.command(command)
        return out.decode(self.defaultEcoding)

    def listDisk(self):
        out = self._execDiskpartCmd('LIST DISK')
        result = re.findall(self._locale.LIST_DISK_PATTERN, out)
        if len(result)==0:
            print out
        for disk in result:
            print disk[0] + ' - ' + disk[1]

    def selectDisk(self, diskID):
        """ Perform SELECT DISK command
        :param diskID: (int) Disk id
        :return: (str) DISK PART output
        Raises:
          DiskpartException: If command is not valid
          ValueError: if diskID not int
        """
        try:
            out = self._execDiskpartCmd("SELECT DISK %d" %int(diskID))
        except ValueError:
            raise DiskUtilExceptions('Select disk : Invalid Disk ID Parameter : <' + diskID + '>')
        if not self._locale.SELECT_DISK_VALIDATION_MESSAGE in out:
            raise DiskUtilExceptions('Cannot select disk : ' + out)

    def listDiskPartition(self, diskID):
        self.selectDisk(diskID)
        out = self._execDiskpartCmd("LIST PARTITION")
        result = re.findall(self._locale.LIST_PARTITION_PATTERN, out)
        if len(result) == 0:
            raise DiskUtilExceptions('List partition : ' + out)
        for partition in result:
            print partition[0] + ' - ' + partition[1]