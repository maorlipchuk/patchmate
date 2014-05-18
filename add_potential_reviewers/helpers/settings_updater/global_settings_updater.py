#!/usr/bin/env python
# -*- coding: utf-8 -*-
from common import SettingsUpdater


class GlobalsSettingsUpdater(SettingsUpdater):
    def update_settings(self):
        self.update_single_module_settings("global")
