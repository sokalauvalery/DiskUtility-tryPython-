# -*- encoding: cp1251 -*-
"""Library contains Diskpart multiple language constants"""
from abc import ABCMeta, abstractproperty

class LocaleInterface():
    __metaclass__ = ABCMeta
    @property
    def LIST_PARTITION_PATTERN(self):
        """
        :return: Pattern for matching LIST PARTITION command output
        """
        raise NotImplementedError
    @property
    def LIST_DISK_PATTERN(self):
        """
        :return: Pattern for matching LIST DISK command output
        """
        raise NotImplementedError

    @property
    def SELECT_DISK_VALIDATION_MESSAGE(self):
        """
        :return: SELECT DISK SUCCESS MESSAGE
        """
        raise NotImplementedError

class RuLocale(LocaleInterface):
    LIST_DISK_PATTERN = u'(���� [0-9]+)\s+.+?\s+([0-9]+\s[G|M|K����]?)'
    LIST_PARTITION_PATTERN = u'(������ [0-9]+).*?([0-9]+ G�|��|��)'
    SELECT_DISK_VALIDATION_MESSAGE = u'������ ����'

class EnLocale(LocaleInterface):
    LIST_DISK_PATTERN = '(Disk [0-9]+)\s+.+?\s+([0-9]+\s[GB|MB|KB|B]?)'
    LIST_PARTITION_PATTERN = '(Partition [0-9]+).*?([0-9]+ GB|MB|KB|B)'
    SELECT_DISK_VALIDATION_MESSAGE = 'is now the selected disk'