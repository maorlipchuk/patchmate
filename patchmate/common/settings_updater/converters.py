#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from patchmate.common.logger import logger


class ConverterException(Exception):
    pass


class ConverterInterface(object):
    def _raise_exception(self, exception_message):
        logger.error(exception_message)
        raise ConverterException(exception_message)

    def convert(self, value):
        raise NotImplementedError()


class StrToStrConverter(ConverterInterface):
    def convert(self, value):
        return str(value)


class StrToBoolConverter(ConverterInterface):
    def convert(self, value):
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        exception_message = "Converting {value} to boolean was failed".format(value=value)
        self._raise_exception(exception_message)


class StrToIntConverter(ConverterInterface):
    def convert(self, value):
        if value.isdigit():
            return int(value)
        exception_message = "Converting {value} to integer was failed".format(value=value)
        self._raise_exception(exception_message)


class StrToFloatConverter(ConverterInterface):
    def convert(self, value):
        try:
            return float(value)
        except ValueError:
            exception_message = "Converting {value} to float was failed".format(value=value)
            self._raise_exception(exception_message)


class StrToListConverter(ConverterInterface):
    def convert(self, value):
        if value.endswith(']') and value.startswith('['):
            return re.split(", |,", value[1:-1])
        else:
            exception_message = "Converting {value} to list failed".format(value=value)
            self._raise_exception(exception_message)
