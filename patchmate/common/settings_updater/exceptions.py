#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ConvertException(Exception):
    pass


class SettingsUpdaterException(Exception):
    pass


class SettingsUpdaterExceptionSettingTypeNotSupported(SettingsUpdaterException):
    pass