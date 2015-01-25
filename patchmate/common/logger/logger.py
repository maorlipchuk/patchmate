#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


logger = logging.getLogger("PatchMate Logger")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("patchmate_logs.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)